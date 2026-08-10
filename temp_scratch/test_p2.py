import urllib.request, urllib.parse, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'

form_data = {
    'page.pageNo': '2',
    'page.orderBy': '',
    'page.order': '',
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

req = urllib.request.Request(
    url,
    data=data,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    
    rows = re.findall(r'<tr[\s\S]*?</tr>', html, re.IGNORECASE)
    print(f"Page 2 Rows: {len(rows)}")
    for j, r in enumerate(rows[1:6], start=1):
        clean_row = re.sub(r'<[^>]+>', ' ', r)
        clean_row = ' '.join(clean_row.split())
        print(f"Row {j}: {clean_row}")
        links = re.findall(r'href=["\'](/perxxgkinfo/xkgkAction!xkgk.action\?[^"\']+)["\']', r)
        print(f"  Link: {links}")
