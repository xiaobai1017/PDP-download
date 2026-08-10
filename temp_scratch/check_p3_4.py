import urllib.request, ssl, csv

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('downloads_manifest.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

row3_4 = [r for r in rows if r['page'] == '3' and r['index'] == '4'][0]
detail_url = row3_4['detail_url']
print("Detail URL for P3-4:", detail_url)

req = urllib.request.Request(detail_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print("Page length:", len(html))
    with open('p3_4_detail.html', 'w', encoding='utf-8') as f_out:
        f_out.write(html)

print("Saved p3_4_detail.html")
