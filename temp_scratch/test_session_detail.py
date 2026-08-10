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

match1 = re.search(r'name=["\']tempReportKey["\']\s+value=["\']([^"\']+)["\']', html1)
temp_key = match1.group(1) if match1 else ''

# Step 2: POST query Jilin Page 3
form_p3 = {
    'page.pageNo': '3',
    'page.orderBy': '',
    'page.order': '',
    'tempReportKey': temp_key,
    'province': '220000000000',
    'city': '',
    'management': '',
    'registerentername': '',
    'xkznum': '',
    'treadname': '',
    'treadcode': '',
    'publishtime': ''
}
data_p3 = urllib.parse.urlencode(form_p3).encode('utf-8')
req2 = urllib.request.Request(init_url, data=data_p3, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Content-Type': 'application/x-www-form-urlencoded'})
with opener.open(req2) as resp:
    html_p3 = resp.read().decode('utf-8', errors='ignore')

# Step 3: Fetch P3-4 detail page (dataid=ff9a8e1a519c4ffc86b7404eed8491e5)
detail_url = 'https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=ff9a8e1a519c4ffc86b7404eed8491e5'
req3 = urllib.request.Request(
    detail_url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': init_url
    }
)
with opener.open(req3) as resp:
    html_detail = resp.read().decode('utf-8', errors='ignore')
    print("Detail page length for P3-4:", len(html_detail))
    
    fb_match = re.search(r'href=["\'](/perxxgkinfo/syssb/xkgg/xkgg!downloadFile\.action\?[^"\']*)["\']', html_detail)
    if fb_match:
        print("Found PDF download link:", fb_match.group(1))
    else:
        print("No PDF download link found. Searching all links in detail page:")
        links = re.findall(r'<a[\s\S]*?>[\s\S]*?</a>', html_detail)
        for l in links:
            print("  Link:", l.strip()[:150])
