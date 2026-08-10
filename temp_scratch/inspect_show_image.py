import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid=500bbe89c72f4691bb45e1f5adac37b9"
print(f"Fetching {url}...")

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=500bbe89c72f4691bb45e1f5adac37b9"
    }
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        print("Status Code:", resp.status)
        print("Content-Type:", resp.headers.get("Content-Type"))
        print("Content-Disposition:", resp.headers.get("Content-Disposition"))
        content = resp.read()
        print("Content length:", len(content))
        with open("showImage_result.html_or_pdf", "wb") as f:
            f.write(content)
        print("Saved to showImage_result.html_or_pdf")
        if len(content) < 2000:
            print("Text snippet:", content.decode('utf-8', errors='ignore'))
except Exception as e:
    print("Error:", e)
