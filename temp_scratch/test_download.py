import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

download_url = 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!downloadFile.action?method=download&fileType=fbfile&datafileid=f2bb66a203a34cecb6c7c1a1c89eec0a&dataid=500bbe89c72f4691bb45e1f5adac37b9'

print(f"Downloading PDF from {download_url}...")

req = urllib.request.Request(
    download_url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=500bbe89c72f4691bb45e1f5adac37b9'
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    headers = dict(resp.headers)
    print("Content-Type:", headers.get('Content-Type'))
    print("Content-Disposition:", headers.get('Content-Disposition'))
    content = resp.read()
    print(f"Downloaded bytes: {len(content)}")
    
    # Save test pdf file
    with open('test_fubun.pdf', 'wb') as f:
        f.write(content)

print("Saved test_fubun.pdf successfully!")
