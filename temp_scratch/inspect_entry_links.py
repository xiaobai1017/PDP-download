import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Search for tab or licenseInformation or forms
matches = re.findall(r'<a[^>]*?licenseInformation[^>]*?>[\s\S]*?</a>', html, re.IGNORECASE)
print("Matches count:", len(matches))
for m in matches:
    print("  Link:", m)

# Search for any form or iframe
iframes = re.findall(r'<iframe[\s\S]*?>', html, re.IGNORECASE)
print("Iframes:", iframes)

forms = re.findall(r'<form[\s\S]*?>', html, re.IGNORECASE)
print("Forms:", forms)
