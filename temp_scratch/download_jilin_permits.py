import urllib.request, urllib.parse, ssl, http.cookiejar
import re
import os
import sys
import time
import csv

# Disable SSL verification for government legacy HTTPS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = 'https://permit.mee.gov.cn'
INIT_URL = f'{BASE_URL}/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
OUTPUT_DIR = r'c:\Users\hubin\workspace\PDP-download\pdf_downloads'
MANIFEST_CSV = r'c:\Users\hubin\workspace\PDP-download\downloads_manifest.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid Windows filename characters"""
    return re.sub(r'[\ \/\:\*\?\"\,\<\>\|]', '_', filename).strip()

def create_opener():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cj)
    )
    return opener

def get_initial_session(opener):
    req = urllib.request.Request(
        INIT_URL,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    )
    with opener.open(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html)
    temp_key = match.group(1) if match else ''
    return temp_key

def fetch_page_data(opener, page_no, temp_key, province_code='220000000000'):
    form_data = {
        'page.pageNo': str(page_no),
        'page.orderBy': '',
        'page.order': '',
        'tempReportKey': temp_key,
        'province': province_code,
        'city': '',
        'management': '',
        'registerentername': '',
        'xkznum': '',
        'treadname': '',
        'treadcode': '',
        'publishtime': ''
    }
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    req = urllib.request.Request(
        INIT_URL,
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': INIT_URL
        }
    )
    with opener.open(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    # Extract updated tempReportKey
    match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html)
    next_temp_key = match.group(1) if match else temp_key
    
    # Extract total pages if available
    total_pages_match = re.search(r'var\s+(?:totalPages|pagesum)\s*=\s*(\d+);', html)
    total_pages = int(total_pages_match.group(1)) if total_pages_match else None

    # Parse rows
    rows = re.findall(r'<tr[\s\S]*?</tr>', html, re.IGNORECASE)
    items = []
    
    # Skip header row (row 0)
    for r in rows[1:]:
        tds = re.findall(r'<td[\s\S]*?>([\s\S]*?)</td>', r, re.IGNORECASE)
        if len(tds) < 8:
            continue
        
        def clean_td(td_content):
            text = re.sub(r'<[^>]+>', ' ', td_content)
            return ' '.join(text.split())
        
        province = clean_td(tds[0])
        city = clean_td(tds[1])
        xkz_num = clean_td(tds[2])
        company_name = clean_td(tds[3])
        industry = clean_td(tds[4])
        valid_period = clean_td(tds[5])
        publish_date = clean_td(tds[6])
        mgmt_type = clean_td(tds[7])
        
        # Link for detail page
        link_match = re.search(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
        detail_url = BASE_URL + link_match.group(1) if link_match else ''
        
        # Extract dataid from detail_url
        dataid_match = re.search(r'dataid=([a-f0-9]+)', detail_url)
        dataid = dataid_match.group(1) if dataid_match else ''
        
        items.append({
            'province': province,
            'city': city,
            'xkz_num': xkz_num,
            'company_name': company_name,
            'industry': industry,
            'valid_period': valid_period,
            'publish_date': publish_date,
            'mgmt_type': mgmt_type,
            'detail_url': detail_url,
            'dataid': dataid
        })
        
    return items, next_temp_key, total_pages

def get_pdf_download_url(opener, detail_url):
    """Fetch enterprise detail page and locate 排污许可证副本 PDF link"""
    if not detail_url:
        return None
    try:
        req = urllib.request.Request(
            detail_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': INIT_URL
            }
        )
        with opener.open(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        if len(html) < 500 and '不能直接访问这个页面' in html:
            # Stale session fallback
            return None
            
        # Find 排污许可证副本 link: search for fileType=fbfile or 副本
        fb_match = re.search(r'href=["\'](/perxxgkinfo/syssb/xkgg/xkgg!downloadFile\.action\?[^"\']*fileType=fbfile[^"\']*)["\']', html)
        if fb_match:
            return BASE_URL + fb_match.group(1)
            
        # Generic downloadFile match
        dl_match = re.search(r'href=["\'](/perxxgkinfo/syssb/xkgg/xkgg!downloadFile\.action\?[^"\']+)["\']', html)
        if dl_match:
            return BASE_URL + dl_match.group(1)
            
        return None
    except Exception as e:
        print(f"  Error fetching detail page {detail_url}: {e}")
        return None

def download_pdf_file(opener, download_url, save_path, referer):
    """Download PDF file to specified path"""
    try:
        req = urllib.request.Request(
            download_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': referer
            }
        )
        with opener.open(req, timeout=30) as resp:
            content = resp.read()
            if len(content) > 100:  # Valid non-empty response
                with open(save_path, 'wb') as f:
                    f.write(content)
                return True, len(content)
            else:
                return False, 0
    except Exception as e:
        print(f"  Error downloading {download_url}: {e}")
        return False, 0

def run_download_job(start_page=1, max_pages=5):
    print("==================================================")
    print(f"Starting PDP Download for Jilin Province (Pages: {start_page} to {max_pages})")
    print("==================================================")
    
    opener = create_opener()
    temp_key = get_initial_session(opener)
    print(f"Session initialized. Initial tempReportKey: {temp_key}")
    
    # If starting from a page > 1, fast-forward tempReportKey page by page
    if start_page > 1:
        print(f"Fast-forwarding session to page {start_page}...")
        for p in range(1, start_page):
            _, temp_key, _ = fetch_page_data(opener, p, temp_key)
            time.sleep(0.2)
            
    # Prepare CSV manifest writer
    file_exists = os.path.exists(MANIFEST_CSV)
    csv_file = open(MANIFEST_CSV, 'a', newline='', encoding='utf-8-sig')
    fieldnames = ['page', 'index', 'province', 'city', 'xkz_num', 'company_name', 'industry', 'valid_period', 'publish_date', 'mgmt_type', 'pdf_filename', 'file_size', 'status', 'detail_url', 'download_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
        
    total_downloaded = 0
    total_failed = 0

    for page_no in range(start_page, max_pages + 1):
        print(f"\n--- Fetching Page {page_no}/{max_pages} ---")
        try:
            items, temp_key, total_pages = fetch_page_data(opener, page_no, temp_key)
            print(f"Page {page_no}: Found {len(items)} enterprises. (Total pages in system: {total_pages})")
            
            for idx, item in enumerate(items, start=1):
                company = item['company_name']
                xkz = item['xkz_num']
                detail_url = item['detail_url']
                
                clean_company = sanitize_filename(company)
                clean_xkz = sanitize_filename(xkz)
                pdf_filename = f"{clean_company}_{clean_xkz}_排污许可证副本.pdf"
                save_path = os.path.join(OUTPUT_DIR, pdf_filename)
                
                # Check if already downloaded
                if os.path.exists(save_path) and os.path.getsize(save_path) > 100:
                    print(f"  [{page_no}-{idx}] [Skipped] Already exists: {pdf_filename}")
                    status = 'SUCCESS (EXISTS)'
                    file_size = os.path.getsize(save_path)
                    download_url = ''
                    total_downloaded += 1
                else:
                    pdf_url = get_pdf_download_url(opener, detail_url)
                    if pdf_url:
                        success, file_size = download_pdf_file(opener, pdf_url, save_path, detail_url)
                        if success:
                            print(f"  [{page_no}-{idx}] [Downloaded] {pdf_filename} ({file_size} bytes)")
                            status = 'SUCCESS'
                            download_url = pdf_url
                            total_downloaded += 1
                        else:
                            print(f"  [{page_no}-{idx}] [Failed] Failed downloading PDF")
                            status = 'FAILED (DOWNLOAD ERROR)'
                            download_url = pdf_url
                            total_failed += 1
                    else:
                        print(f"  [{page_no}-{idx}] [Failed] No PDF download link found")
                        status = 'FAILED (NO PDF LINK)'
                        file_size = 0
                        download_url = ''
                        total_failed += 1
                
                # Log to CSV manifest
                writer.writerow({
                    'page': page_no,
                    'index': idx,
                    'province': item['province'],
                    'city': item['city'],
                    'xkz_num': item['xkz_num'],
                    'company_name': item['company_name'],
                    'industry': item['industry'],
                    'valid_period': item['valid_period'],
                    'publish_date': item['publish_date'],
                    'mgmt_type': item['mgmt_type'],
                    'pdf_filename': pdf_filename,
                    'file_size': file_size,
                    'status': status,
                    'detail_url': detail_url,
                    'download_url': download_url
                })
                csv_file.flush()
                time.sleep(0.3)  # Be polite to the server
                
        except Exception as e:
            print(f"Error processing page {page_no}: {e}")
            
    csv_file.close()
    print("\n==================================================")
    print(f"Job completed! Total Downloaded/Existing: {total_downloaded}, Total Failed: {total_failed}")
    print(f"PDF files saved in: {OUTPUT_DIR}")
    print(f"Manifest CSV saved in: {MANIFEST_CSV}")
    print("==================================================")

if __name__ == '__main__':
    start_p = 1
    max_p = 5
    if len(sys.argv) > 1:
        start_p = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_p = int(sys.argv[2])
    run_download_job(start_p, max_p)
