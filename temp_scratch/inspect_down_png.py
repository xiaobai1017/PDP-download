from curl_cffi import requests

session = requests.Session(impersonate="chrome120")
session.proxies = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
dataid = "3027bbe26ab04da383068c3d7f1973eb"
show_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"

# 1. Fetch showImage
r_show = session.get(show_url, headers={"User-Agent": UA}, timeout=15)
print("showImage text snippet:", r_show.text[:500])

import re
img_count_m = re.search(r'id="imgCount"\s+value="(\d+)"', r_show.text)
pkid_m = re.search(r'id="pkid"\s+value="([^"]+)"', r_show.text)

img_count = int(img_count_m.group(1)) if img_count_m else 0
pkid = pkid_m.group(1) if pkid_m else ""
print(f"imgCount: {img_count}, pkid: {pkid}")

# 2. Fetch page 1 vs page 4
for i in [1, 2, 4]:
    img_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{i}&fileType=pdffile&dataid={dataid}"
    r_img = session.get(img_url, headers={"User-Agent": UA, "Referer": show_url}, timeout=15)
    print(f"Page {i}: status={r_img.status_code}, len={len(r_img.content)}, Content-Type={r_img.headers.get('Content-Type')}")
    if len(r_img.content) < 1000:
        print("  Text snippet:", r_img.text)
