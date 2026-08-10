import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=500bbe89c72f4691bb45e1f5adac37b9'
print(f"Fetching detail page: {url}")

req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print(f"Status: {resp.status}, length: {len(html)}")
    with open('detail_page.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Saved detail_page.html")
