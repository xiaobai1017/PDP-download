from curl_cffi import requests
import re

session = requests.Session(impersonate="chrome120")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
ENTRY_URL = "https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action"
INIT_URL = "https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
BASE_URL = "https://permit.mee.gov.cn"

# 0. GET ENTRY_URL
print("0. GET ENTRY_URL...")
r_entry = session.get(ENTRY_URL, headers={"User-Agent": UA})
print("ENTRY_URL size:", len(r_entry.text))

# 1. GET INIT_URL with Referer: ENTRY_URL
print("1. GET INIT_URL...")
r_init = session.get(INIT_URL, headers={"User-Agent": UA, "Referer": ENTRY_URL})
print("INIT_URL size:", len(r_init.text))

match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', r_init.text)
temp_key = match.group(1) if match else ''
print("tempReportKey:", temp_key)

if temp_key:
    # 2. POST Page 1 query
    print("2. POST Page 1 query...")
    post_data = {
        'page.pageNo': '1', 'page.orderBy': '', 'page.order': '',
        'tempReportKey': temp_key, 'province': '220000000000',
        'city': '', 'management': '', 'registerentername': '',
        'xkznum': '', 'treadname': '', 'treadcode': '', 'publishtime': ''
    }
    r_p1 = session.post(INIT_URL, data=post_data, headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded", "Referer": INIT_URL})
    print("Page 1 result size:", len(r_p1.text))

    rows = re.findall(r'<tr[\s\S]*?</tr>', r_p1.text, re.IGNORECASE)
    print("Found rows:", len(rows)-1)

    for idx, r in enumerate(rows[1:3], start=1):
        tds = re.findall(r'<td[\s\S]*?>([\s\S]*?)</td>', r, re.IGNORECASE)
        if len(tds) < 8: continue
        company = re.sub(r'<[^>]+>', '', tds[3]).strip()
        link_m = re.search(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
        detail_url = BASE_URL + link_m.group(1) if link_m else ''
        dataid_m = re.search(r'dataid=([a-f0-9]+)', detail_url)
        dataid = dataid_m.group(1) if dataid_m else ''

        print(f"\n--- Enterprise {idx}: {company} (dataid={dataid}) ---")
        
        # 3. GET detail_url
        r_det = session.get(detail_url, headers={"User-Agent": UA, "Referer": INIT_URL})
        print("Detail status:", r_det.status_code, "len:", len(r_det.text))
        
        # 4. GET show_url
        show_url = f"{BASE_URL}/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"
        r_show = session.get(show_url, headers={"User-Agent": UA, "Referer": detail_url})
        print("showImage status:", r_show.status_code, "len:", len(r_show.text))
        
        img_count_m = re.search(r'id="imgCount"\s+value="(\d+)"', r_show.text)
        pkid_m = re.search(r'id="pkid"\s+value="([^"]+)"', r_show.text)
        img_count = int(img_count_m.group(1)) if img_count_m else 0
        pkid = pkid_m.group(1) if pkid_m else ""
        print(f"imgCount: {img_count}, pkid: {pkid}")
        
        # 5. GET downFilePng for pages 1..3
        for p_i in [1, 2, 3]:
            img_url = f"{BASE_URL}/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{p_i}&fileType=pdffile&dataid={dataid}"
            r_img = session.get(img_url, headers={"User-Agent": UA, "Referer": show_url})
            print(f"  Page {p_i}: status={r_img.status_code}, len={len(r_img.content)}, Content-Type={r_img.headers.get('Content-Type')}")
