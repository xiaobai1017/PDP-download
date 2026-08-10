import urllib.request, urllib.parse, ssl, http.cookiejar, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj)
)

# Step 1: GET initial page
init_url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
print("1. GET initial page...")
req1 = urllib.request.Request(init_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with opener.open(req1) as resp:
    html1 = resp.read().decode('utf-8', errors='ignore')

# Extract tempReportKey
match1 = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html1)
temp_key1 = match1.group(1) if match1 else ''
print("Initial tempReportKey:", temp_key1)

# Step 2: POST query for Jilin Page 1
print("\n2. POST query Jilin Page 1...")
form_p1 = {
    'page.pageNo': '1',
    'page.orderBy': '',
    'page.order': '',
    'tempReportKey': temp_key1,
    'province': '220000000000',
    'city': '',
    'management': '',
    'registerentername': '',
    'xkznum': '',
    'treadname': '',
    'treadcode': '',
    'publishtime': ''
}
data_p1 = urllib.parse.urlencode(form_p1).encode('utf-8')
req2 = urllib.request.Request(init_url, data=data_p1, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Content-Type': 'application/x-www-form-urlencoded'})
with opener.open(req2) as resp:
    html_p1 = resp.read().decode('utf-8', errors='ignore')

match2 = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html_p1)
temp_key2 = match2.group(1) if match2 else temp_key1
print("Page 1 tempReportKey:", temp_key2)

# Step 3: POST query for Jilin Page 2
print("\n3. POST query Jilin Page 2...")
form_p2 = {
    'page.pageNo': '2',
    'page.orderBy': '',
    'page.order': '',
    'tempReportKey': temp_key2,
    'province': '220000000000',
    'city': '',
    'management': '',
    'registerentername': '',
    'xkznum': '',
    'treadname': '',
    'treadcode': '',
    'publishtime': ''
}
data_p2 = urllib.parse.urlencode(form_p2).encode('utf-8')
req3 = urllib.request.Request(init_url, data=data_p2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Content-Type': 'application/x-www-form-urlencoded'})
with opener.open(req3) as resp:
    html_p2 = resp.read().decode('utf-8', errors='ignore')

rows = re.findall(r'<tr[\s\S]*?</tr>', html_p2, re.IGNORECASE)
print(f"Page 2 Rows: {len(rows)}")
for j, r in enumerate(rows[1:6], start=1):
    clean_row = re.sub(r'<[^>]+>', ' ', r)
    clean_row = ' '.join(clean_row.split())
    print(f"Row {j}: {clean_row}")
    links = re.findall(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
    print(f"  Link: {links}")
