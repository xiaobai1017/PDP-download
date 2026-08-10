import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dataid = "500bbe89c72f4691bb45e1f5adac37b9"
pkid = "c6d5a56acd1e4177903b71e2a66dd55c"
page_i = 1

img_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{page_i}&fileType=pdffile&dataid={dataid}"
print(f"Fetching 副本 page 1 image from {img_url}...")

req = urllib.request.Request(
    img_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    print("Content-Type:", resp.headers.get("Content-Type"))
    content = resp.read()
    print("Image bytes received:", len(content))
    with open("fubun_p1.png", "wb") as f:
        f.write(content)

print("Saved fubun_p1.png successfully!")
