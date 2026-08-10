import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE = "https://permit.mee.gov.cn"
dataid = "500bbe89c72f4691bb45e1f5adac37b9"

INIT_URL = f"{BASE}/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
detail_url = f"{BASE}/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid={dataid}"

req = urllib.request.Request(
    detail_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": INIT_URL
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print("All <a> links on detail page:")
matches = re.findall(r'<a[^>]*?>[\s\S]*?</a>', html, re.IGNORECASE)
for m in matches:
    clean_text = re.sub(r'<[^>]+>', '', m).strip()
    href_m = re.search(r'href=["\']([^"\']+)["\']', m, re.IGNORECASE)
    href = href_m.group(1) if href_m else ''
    print(f"  Text: '{clean_text}'")
    print(f"  Href: {href}")
    print("  " + "-"*50)
