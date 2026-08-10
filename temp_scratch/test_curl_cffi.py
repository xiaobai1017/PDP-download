from curl_cffi import requests
import re

session = requests.Session(impersonate="chrome120")

url = "https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
print(f"Fetching {url} with curl_cffi impersonate=chrome120...")

resp = session.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache"
    },
    timeout=15
)

print(f"Status Code: {resp.status_code}")
print(f"Response Length: {len(resp.text)}")

if "tempReportKey" in resp.text:
    match = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', resp.text)
    print("SUCCESS! Found tempReportKey:", match.group(1) if match else "None")
else:
    print("Snippet:", resp.text[:300])
