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
ENTRY_URL = 'https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action'
LICENSE_URL = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
BASE_URL = 'https://permit.mee.gov.cn'

print("1. GET portal entry page...")
req1 = urllib.request.Request(ENTRY_URL, headers={'User-Agent': UA})
with opener.open(req1) as resp:
    html1 = resp.read().decode('utf-8', errors='ignore')
print("Portal entry HTML size:", len(html1))

print("2. GET license page with Referer: ENTRY_URL...")
req2 = urllib.request.Request(LICENSE_URL, headers={'User-Agent': UA, 'Referer': ENTRY_URL})
with opener.open(req2) as resp:
    html2 = resp.read().decode('utf-8', errors='ignore')
print("License page size:", len(html2))

match2 = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html2)
temp_key = match2.group(1) if match2 else ''
print("Initial tempReportKey:", temp_key)

if temp_key:
    # POST Page 1 query
    print("3. POST Query Jilin Province Page 1...")
    form_data = {
        'page.pageNo': '1',
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
        LICENSE_URL,
        data=data,
        headers={
            'User-Agent': UA,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': LICENSE_URL
        }
    )
    with opener.open(req_p) as resp:
        html_p = resp.read().decode('utf-8', errors='ignore')
    print("Page 1 result size:", len(html_p))
    
    rows = re.findall(r'<tr[\s\S]*?</tr>', html_p, re.IGNORECASE)
    print("Found rows:", len(rows)-1)
