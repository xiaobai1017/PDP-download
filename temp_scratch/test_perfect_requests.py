import urllib.request, urllib.parse, ssl, http.cookiejar, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj)
)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
INIT_URL = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
BASE_URL = 'https://permit.mee.gov.cn'

print("1. GET initial page without referer...")
req1 = urllib.request.Request(INIT_URL, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
with opener.open(req1) as resp:
    html1 = resp.read().decode('utf-8', errors='ignore')

print("Initial HTML size:", len(html1))
match1 = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html1)
temp_key = match1.group(1) if match1 else ''
print("Initial tempReportKey:", temp_key)

# Loop pages 1, 2, 3
for page_no in range(1, 4):
    print(f"\n--- Testing Page {page_no} ---")
    form_data = {
        'page.pageNo': str(page_no),
        'page.orderBy': '',
        'page.order': '',
        'tempReportKey': temp_key,
        'province': '220000000000',
        'city': '',
        'management': '',
        'registerentername': '',
        'xkznum': '',
        'treadname': '',
        'treadcode': '',
        'publishtime': ''
    }
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    req_p = urllib.request.Request(
        INIT_URL,
        data=data,
        headers={
            'User-Agent': UA,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': INIT_URL
        }
    )
    with opener.open(req_p) as resp:
        html_p = resp.read().decode('utf-8', errors='ignore')
        
    match_k = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html_p)
    temp_key = match_k.group(1) if match_k else temp_key
    print(f"Page {page_no} returned size {len(html_p)}, next tempKey: {temp_key}")

    # Parse rows
    rows = re.findall(r'<tr[\s\S]*?</tr>', html_p, re.IGNORECASE)
    print(f"Page {page_no} found {len(rows)-1} enterprise rows.")

    for idx, r in enumerate(rows[1:4], start=1):
        tds = re.findall(r'<td[\s\S]*?>([\s\S]*?)</td>', r, re.IGNORECASE)
        if len(tds) < 8: continue
        company = re.sub(r'<[^>]+>', '', tds[3]).strip()
        link_match = re.search(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
        detail_url = BASE_URL + link_match.group(1) if link_match else ''
        print(f"  [{page_no}-{idx}] {company} -> {detail_url}")

        # Fetch detail page with Referer: INIT_URL
        req_det = urllib.request.Request(detail_url, headers={'User-Agent': UA, 'Referer': INIT_URL})
        with opener.open(req_det) as resp_det:
            html_det = resp_det.read().decode('utf-8', errors='ignore')
            
        fb_match = re.search(r'href=["\'](/perxxgkinfo/syssb/xkgg/xkgg!downloadFile\.action\?[^"\']*)["\']', html_det)
        if fb_match:
            pdf_url = BASE_URL + fb_match.group(1)
            print(f"    -> FOUND PDF LINK: {pdf_url[:80]}...")
            req_pdf = urllib.request.Request(pdf_url, headers={'User-Agent': UA, 'Referer': detail_url})
            with opener.open(req_pdf) as resp_pdf:
                pdf_bytes = resp_pdf.read()
                print(f"    -> DOWNLOAD SUCCESS: {len(pdf_bytes)} bytes!")
        else:
            print(f"    -> Detail page size: {len(html_det)} bytes. No PDF link match.")
