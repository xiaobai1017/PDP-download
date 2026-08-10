import urllib.request, urllib.parse, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'

form_data = {
    'page.pageNo': '1',
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
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print(f"Response status: {resp.status}, length: {len(html)}")
    with open('query_jilin_p1.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved query_jilin_p1.html")
