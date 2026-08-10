import urllib.request, urllib.parse, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!getRegions.action'
data = urllib.parse.urlencode({'parentCode': '000000000000'}).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Provinces:")
    for item in res.get('regions', []):
        print(f"Code: {item.get('regioncode')}, Name: {item.get('regionname')}")
