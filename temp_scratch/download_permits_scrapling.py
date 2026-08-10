import sys
import os
import re
import time
import io
import csv
import random
import socket
import argparse
from pathlib import Path
from curl_cffi import requests
from PIL import Image

BASE_URL = 'https://permit.mee.gov.cn'
ENTRY_URL = f'{BASE_URL}/permitExt/defaults/default-index!getInformation.action'
LICENSE_URL = f'{BASE_URL}/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
OUTPUT_DIR = r'c:\Users\hubin\workspace\PDP-download\pdf_downloads'
MANIFEST_CSV = r'c:\Users\hubin\workspace\PDP-download\downloads_manifest.csv'

PROVINCES = {
    "北京": "110000000000", "北京市": "110000000000",
    "天津": "120000000000", "天津市": "120000000000",
    "河北": "130000000000", "河北省": "130000000000",
    "山西": "140000000000", "山西省": "140000000000",
    "内蒙古": "150000000000", "内蒙古自治区": "150000000000",
    "辽宁": "210000000000", "辽宁省": "210000000000",
    "吉林": "220000000000", "吉林省": "220000000000",
    "黑龙江": "230000000000", "黑龙江省": "230000000000",
    "上海": "310000000000", "上海市": "310000000000",
    "江苏": "320000000000", "江苏省": "320000000000",
    "浙江": "330000000000", "浙江省": "330000000000",
    "安徽": "340000000000", "安徽省": "340000000000",
    "福建": "350000000000", "福建省": "350000000000",
    "江西": "360000000000", "江西省": "360000000000",
    "山东": "370000000000", "山东省": "370000000000",
    "河南": "410000000000", "河南省": "410000000000",
    "湖北": "420000000000", "湖北省": "420000000000",
    "湖南": "430000000000", "湖南省": "430000000000",
    "广东": "440000000000", "广东省": "440000000000",
    "广西": "450000000000", "广西壮族自治区": "450000000000",
    "海南": "460000000000", "海南省": "460000000000",
    "重庆": "500000000000", "重庆市": "500000000000",
    "四川": "510000000000", "四川省": "510000000000",
    "贵州": "520000000000", "贵州省": "520000000000",
    "云南": "530000000000", "云南省": "530000000000",
    "西藏": "540000000000", "西藏自治区": "540000000000",
    "陕西": "610000000000", "陕西省": "610000000000",
    "甘肃": "620000000000", "甘肃省": "620000000000",
    "青海": "630000000000", "青海省": "630000000000",
    "宁夏": "640000000000", "宁夏回族自治区": "640000000000",
    "新疆": "650000000000", "新疆维吾尔自治区": "650000000000",
    "兵团": "660000000000", "新疆生产建设兵团": "660000000000"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

def detect_local_proxy():
    """Auto-detect active local proxy ports if no explicit proxy is passed"""
    ports = [7897, 7890, 10809, 1080, 8080]
    for p in ports:
        try:
            s = socket.socket()
            s.settimeout(0.3)
            s.connect(('127.0.0.1', p))
            s.close()
            print(f"[Proxy Auto-Detect] Found active local proxy on http://127.0.0.1:{p}")
            return f"http://127.0.0.1:{p}"
        except:
            pass
    return None

def sanitize_filename(filename):
    return re.sub(r'[\ \/\:\*\?\"\,\<\>\|]', '_', filename).strip()

def random_wait(min_s=1.5, max_s=3.5):
    time.sleep(random.uniform(min_s, max_s))

class RobustPermitDownloader:
    def __init__(self, province="吉林", proxy=None, start_page=1, max_pages=5, max_img_pages=50):
        # Resolve province code
        if province in PROVINCES:
            self.province_name = province
            self.province_code = PROVINCES[province]
        elif len(province) == 12 and province.isdigit():
            self.province_code = province
            # Find name from code
            self.province_name = [k for k, v in PROVINCES.items() if v == province and len(k) <= 4][0]
        else:
            print(f"[Warn] Unknown province '{province}', defaulting to 吉林省")
            self.province_name = "吉林"
            self.province_code = "220000000000"

        if not proxy:
            proxy = detect_local_proxy()
        self.proxy = proxy
        self.start_page = start_page
        self.max_pages = max_pages
        self.max_img_pages = max_img_pages
        
        # Save to province subfolder
        self.output_dir = os.path.join(OUTPUT_DIR, self.province_name)
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.proxies_dict = None
        if self.proxy:
            self.proxies_dict = {"http": self.proxy, "https": self.proxy}

    def create_session(self):
        session = requests.Session(impersonate="chrome120")
        if self.proxies_dict:
            session.proxies = self.proxies_dict
        return session

    def fetch_with_retry(self, session, url, method="GET", data=None, headers=None, max_retries=3):
        for attempt in range(1, max_retries + 1):
            try:
                if method.upper() == "POST":
                    resp = session.post(url, data=data, headers=headers, timeout=25)
                else:
                    resp = session.get(url, headers=headers, timeout=25)

                html = resp.text
                if len(html) < 600 and ("不能直接访问" in html or "errorinfo.jsp" in resp.url or "阻断" in html):
                    print(f"  [WAF 458 Intercepted] Attempt {attempt}/{max_retries}: Server returned 458 block page. Retrying...")
                    random_wait(3.0, 6.0)
                    session = self.create_session()
                    continue
                return resp, html, session
            except Exception as e:
                print(f"  [Network Exception] Attempt {attempt}/{max_retries}: {e}")
                random_wait(3.0, 6.0)
        return None, "", session

    def download_fubun_pdf(self, session, dataid, detail_url, save_path, ua):
        """
        Download 排污许可证副本 PDF
        """
        show_image_url = f"{BASE_URL}/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"
        print(f"    -> Accessing 排污许可证副本 page: {show_image_url}...")
        
        headers = {"User-Agent": ua, "Referer": detail_url}
        resp, show_html, session = self.fetch_with_retry(session, show_image_url, headers=headers)

        img_count_m = re.search(r'id="imgCount"\s+value="(\d+)"', show_html)
        pkid_m = re.search(r'id="pkid"\s+value="([^"]+)"', show_html)

        img_count = int(img_count_m.group(1)) if img_count_m else 0
        pkid = pkid_m.group(1) if pkid_m else ""

        if img_count == 0 or not pkid:
            print(f"    -> [Notice] No 副本 image pages generated yet or missing pkid.")
            return False, 0, session

        pil_images = []
        pages_to_fetch = min(img_count, self.max_img_pages)
        print(f"    -> Downloading {pages_to_fetch}/{img_count} pages of 排污许可证副本...")

        for i in range(1, pages_to_fetch + 1):
            img_url = f"{BASE_URL}/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{i}&fileType=pdffile&dataid={dataid}"
            img_headers = {"User-Agent": ua, "Referer": show_image_url}
            
            try:
                r_img = session.get(img_url, headers=img_headers, timeout=20)
                if r_img.status_code == 200 and len(r_img.content) > 1000:
                    img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                    pil_images.append(img)
                else:
                    print(f"      [Warn] Page {i} download failed (HTTP {r_img.status_code})")
            except Exception as img_err:
                print(f"      [Error] Page {i} error: {img_err}")
                
            time.sleep(0.3)

        if pil_images:
            pil_images[0].save(save_path, "PDF", resolution=100.0, save_all=True, append_images=pil_images[1:])
            file_size = os.path.getsize(save_path)
            print(f"    -> [SUCCESS] Merged {len(pil_images)} pages into 排污许可证副本 PDF: ({file_size} bytes)")
            return True, file_size, session
        else:
            return False, 0, session

    def run(self):
        print("==================================================")
        print(f"Starting Multi-Province PDP Permit Downloader")
        print(f"Selected Region: {self.province_name} (Code: {self.province_code})")
        print(f"Target Pages: {self.start_page} to {self.max_pages}")
        print(f"Proxy Setting: {self.proxy if self.proxy else 'Direct Connection'}")
        print(f"Output Directory: {self.output_dir}")
        print("==================================================")

        session = self.create_session()
        ua = random.choice(USER_AGENTS)

        # Step 1: GET Entry Page
        print(f"[1/3] Navigating to portal entry: {ENTRY_URL}")
        entry_headers = {"User-Agent": ua, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        _, entry_html, session = self.fetch_with_retry(session, ENTRY_URL, headers=entry_headers)
        random_wait(1.5, 2.5)

        # Step 2: GET License Information page
        print(f"[2/3] Fetching license search interface: {LICENSE_URL}")
        lic_headers = {"User-Agent": ua, "Referer": ENTRY_URL, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        _, lic_html, session = self.fetch_with_retry(session, LICENSE_URL, headers=lic_headers)

        match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', lic_html)
        temp_key = match.group(1) if match else ''

        if not temp_key:
            print("\n[WAF ALERT] Server returned WAF 458 block page.")
            print("Your IP or proxy node is currently rate-limited by government WAF.")
            print("Tip: Switch proxy node in Clash/V2Ray or pass `--proxy http://127.0.0.1:7897`.")
            return

        print(f"[3/3] Session established. Initial tempReportKey: {temp_key}")

        # CSV Manifest
        file_exists = os.path.exists(MANIFEST_CSV)
        csv_file = open(MANIFEST_CSV, 'a', newline='', encoding='utf-8-sig')
        fieldnames = [
            'page', 'index', 'province', 'city', 'xkz_num', 'company_name',
            'industry', 'valid_period', 'publish_date', 'mgmt_type',
            'pdf_filename', 'file_size', 'status', 'detail_url', 'download_url'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        total_downloaded = 0
        total_failed = 0

        # Fast forward if start_page > 1
        if self.start_page > 1:
            print(f"[Engine] Fast-forwarding session to page {self.start_page} for {self.province_name}...")
            for p in range(1, self.start_page):
                post_data = {
                    'page.pageNo': str(p), 'page.orderBy': '', 'page.order': '',
                    'tempReportKey': temp_key, 'province': self.province_code,
                    'city': '', 'management': '', 'registerentername': '',
                    'xkznum': '', 'treadname': '', 'treadcode': '', 'publishtime': ''
                }
                p_headers = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded", "Referer": LICENSE_URL}
                _, p_html, session = self.fetch_with_retry(session, LICENSE_URL, method="POST", data=post_data, headers=p_headers)
                match_k = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', p_html)
                if match_k: temp_key = match_k.group(1)
                random_wait(1.5, 2.5)

        for current_p in range(self.start_page, self.max_pages + 1):
            print(f"\n--- Processing {self.province_name} Page {current_p}/{self.max_pages} ---")
            post_data = {
                'page.pageNo': str(current_p), 'page.orderBy': '', 'page.order': '',
                'tempReportKey': temp_key, 'province': self.province_code,
                'city': '', 'management': '', 'registerentername': '',
                'xkznum': '', 'treadname': '', 'treadcode': '', 'publishtime': ''
            }
            p_headers = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded", "Referer": LICENSE_URL}
            _, p_html, session = self.fetch_with_retry(session, LICENSE_URL, method="POST", data=post_data, headers=p_headers)

            match_k = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', p_html)
            if match_k: temp_key = match_k.group(1)

            rows = re.findall(r'<tr[\s\S]*?</tr>', p_html, re.IGNORECASE)
            items = []
            for r in rows[1:]:
                tds = re.findall(r'<td[\s\S]*?>([\s\S]*?)</td>', r, re.IGNORECASE)
                if len(tds) < 8: continue
                def clean(t): return ' '.join(re.sub(r'<[^>]+>', ' ', t).split())
                company = clean(tds[3])
                xkz = clean(tds[2])
                link_match = re.search(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
                detail_url = BASE_URL + link_match.group(1) if link_match else ''
                dataid_m = re.search(r'dataid=([a-f0-9]+)', detail_url)
                dataid = dataid_m.group(1) if dataid_m else ''
                
                items.append({
                    'province': clean(tds[0]), 'city': clean(tds[1]), 'xkz_num': xkz,
                    'company_name': company, 'industry': clean(tds[4]),
                    'valid_period': clean(tds[5]), 'publish_date': clean(tds[6]),
                    'mgmt_type': clean(tds[7]), 'detail_url': detail_url, 'dataid': dataid
                })

            print(f"Page {current_p}: Found {len(items)} records for {self.province_name}.")

            for idx, item in enumerate(items, start=1):
                company = item['company_name']
                xkz = item['xkz_num']
                detail_url = item['detail_url']
                dataid = item['dataid']
                clean_company = sanitize_filename(company)
                clean_xkz = sanitize_filename(xkz)
                pdf_filename = f"{clean_company}_{clean_xkz}_排污许可证副本.pdf"
                save_path = os.path.join(self.output_dir, pdf_filename)

                # Skip if already downloaded
                if os.path.exists(save_path) and os.path.getsize(save_path) > 100:
                    print(f"  [{current_p}-{idx}] [Skipped] Already downloaded: {pdf_filename}")
                    writer.writerow({
                        'page': current_p, 'index': idx, 'province': item['province'], 'city': item['city'],
                        'xkz_num': item['xkz_num'], 'company_name': item['company_name'], 'industry': item['industry'],
                        'valid_period': item['valid_period'], 'publish_date': item['publish_date'], 'mgmt_type': item['mgmt_type'],
                        'pdf_filename': pdf_filename, 'file_size': os.path.getsize(save_path),
                        'status': 'SUCCESS (EXISTS)', 'detail_url': detail_url, 'download_url': ''
                    })
                    csv_file.flush()
                    total_downloaded += 1
                    continue

                print(f"  [{current_p}-{idx}] Processing 排污许可证副本 for {company} ({xkz})...")
                success, file_size, session = self.download_fubun_pdf(session, dataid, detail_url, save_path, ua)

                if success:
                    status = 'SUCCESS'
                    total_downloaded += 1
                else:
                    status = 'FAILED (NO FUBUN DATA)'
                    file_size = 0
                    total_failed += 1

                writer.writerow({
                    'page': current_p, 'index': idx, 'province': item['province'], 'city': item['city'],
                    'xkz_num': item['xkz_num'], 'company_name': item['company_name'], 'industry': item['industry'],
                    'valid_period': item['valid_period'], 'publish_date': item['publish_date'], 'mgmt_type': item['mgmt_type'],
                    'pdf_filename': pdf_filename, 'file_size': file_size,
                    'status': status, 'detail_url': detail_url,
                    'download_url': f"{BASE_URL}/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"
                })
                csv_file.flush()
                random_wait(2.0, 4.0)

        csv_file.close()
        print("\n==================================================")
        print("Job Finished!")
        print(f"Province: {self.province_name}")
        print(f"Total Downloaded/Existing: {total_downloaded}, Total Failed: {total_failed}")
        print(f"PDF Output Directory: {self.output_dir}")
        print("==================================================")

def main():
    parser = argparse.ArgumentParser(description="Multi-Province PDP Permit Copy PDF Downloader")
    parser.add_argument("--province", type=str, default="吉林", help="Province name or code (e.g. 北京, 广东, 四川, 江苏, 220000000000)")
    parser.add_argument("--start-page", type=int, default=1, help="Start page number")
    parser.add_argument("--max-pages", type=int, default=5, help="Max page number")
    parser.add_argument("--proxy", type=str, default="", help="HTTP/HTTPS proxy URL (e.g. http://127.0.0.1:7897)")
    args = parser.parse_args()

    downloader = RobustPermitDownloader(
        province=args.province,
        proxy=args.proxy,
        start_page=args.start_page,
        max_pages=args.max_pages
    )
    downloader.run()

if __name__ == '__main__':
    main()
