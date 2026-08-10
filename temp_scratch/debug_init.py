import urllib.request, ssl, http.cookiejar, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj)
)

# Step 1: GET entry page
entry_url = 'https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action'
req1 = urllib.request.Request(entry_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with opener.open(req1) as resp:
    html1 = resp.read().decode('utf-8', errors='ignore')
print("Entry page size:", len(html1))

# Step 2: GET licenseInformation.action with Referer: entry_url
license_url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
req2 = urllib.request.Request(
    license_url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': entry_url
    }
)
with opener.open(req2) as resp:
    html2 = resp.read().decode('utf-8', errors='ignore')
print("License page size:", len(html2))

keys = re.findall(r'.{0,50}tempReportKey.{0,50}', html2)
for k in keys:
    print("Key line:", k.strip())
