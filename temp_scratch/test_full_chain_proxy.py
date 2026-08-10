from curl_cffi import requests
import re

session = requests.Session(impersonate="chrome120")
session.proxies = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
ENTRY_URL = "https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action"
LICENSE_URL = "https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"

print("1. Fetching ENTRY_URL with proxy...")
r1 = session.get(ENTRY_URL, headers={"User-Agent": UA}, timeout=15)
print("ENTRY_URL status:", r1.status_code, "length:", len(r1.text))
print("Cookies after entry:", dict(session.cookies))

print("2. Fetching LICENSE_URL with proxy and Referer: ENTRY_URL...")
r2 = session.get(LICENSE_URL, headers={"User-Agent": UA, "Referer": ENTRY_URL}, timeout=15)
print("LICENSE_URL status:", r2.status_code, "length:", len(r2.text))

match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', r2.text)
if match:
    print("SUCCESS!! Found tempReportKey:", match.group(1))
else:
    print("Snippet of LICENSE_URL response:", r2.text[:300])
