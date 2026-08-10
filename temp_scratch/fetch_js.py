import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = 'https://permit.mee.gov.cn'
js_urls = [
    '/permitExt/outside/js/main.js',
    '/permitExt/outside/js/scroll.js',
    '/permitExt/js/urlhanzi.js'
]

for rel in js_urls:
    url = base_url + rel
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"Size: {len(content)}")
            with open(rel.split('/')[-1], 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
