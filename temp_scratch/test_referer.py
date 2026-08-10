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
req1 = urllib.request.Request(init_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with opener.open(req1) as resp:
    html1 = resp.read().decode('utf-8', errors='ignore')

# Step 2: Fetch detail URL with Referer header
detail_url = 'https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=ff9a8e1a519c4ffc86b7404eed8491e5'
req2 = urllib.request.Request(
    detail_url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': init_url
    }
)
with opener.open(req2) as resp:
    html2 = resp.read().decode('utf-8', errors='ignore')
    print("Response length with Referer header:", len(html2))
    
    # Check for download link
    fb_match = re.search(r'href=["\'](/perxxgkinfo/syssb/xkgg/xkgg!downloadFile\.action\?[^"\']*)["\']', html2)
    if fb_match:
        print("Found download link:", fb_match.group(1))
    else:
        print("No download link match. HTML snippet:", html2[:500])
