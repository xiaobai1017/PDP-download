from curl_cffi import requests
import re

session = requests.Session(impersonate="chrome120")
session.proxies = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
dataid = "3027bbe26ab04da383068c3d7f1973eb"
INIT_URL = "https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
detail_url = f"https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid={dataid}"
show_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"

# Step 0: GET INIT_URL
session.get(INIT_URL, headers={"User-Agent": UA})

# Step 1: GET detail_url
print("1. Fetching detail_url...")
r_det = session.get(detail_url, headers={"User-Agent": UA, "Referer": INIT_URL}, timeout=15)
print("Detail status:", r_det.status_code, "len:", len(r_det.text))

# Step 2: Fetch show_url
print("2. Fetching show_url...")
r_show = session.get(show_url, headers={"User-Agent": UA, "Referer": detail_url}, timeout=15)
print("show_url status:", r_show.status_code, "len:", len(r_show.text))

img_count_m = re.search(r'id="imgCount"\s+value="(\d+)"', r_show.text)
pkid_m = re.search(r'id="pkid"\s+value="([^"]+)"', r_show.text)
img_count = int(img_count_m.group(1)) if img_count_m else 0
pkid = pkid_m.group(1) if pkid_m else ""
print(f"imgCount: {img_count}, pkid: {pkid}")

# Step 3: Fetch pages 1, 2, 3
for i in [1, 2, 3]:
    img_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{i}&fileType=pdffile&dataid={dataid}"
    r_img = session.get(img_url, headers={"User-Agent": UA, "Referer": show_url}, timeout=15)
    print(f"Page {i}: status={r_img.status_code}, len={len(r_img.content)}, Content-Type={r_img.headers.get('Content-Type')}")
