import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'
print(f"Fetching {url}...")

req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}")
        print(f"Content Length: {len(content)}")
        with open('license_info.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Saved to license_info.html")
except Exception as e:
    print(f"Error: {e}")
