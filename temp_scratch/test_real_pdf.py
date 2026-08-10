import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pdf_url = "https://permit.mee.gov.cn/perxxgkinfo/syssb/xxgk/xxgk!downloadFilePdf.action?dataid=500bbe89c72f4691bb45e1f5adac37b9"
print(f"Downloading actual PDF from {pdf_url}...")

req = urllib.request.Request(
    pdf_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid=500bbe89c72f4691bb45e1f5adac37b9"
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    print("Content-Type:", resp.headers.get("Content-Type"))
    print("Content-Disposition:", resp.headers.get("Content-Disposition"))
    content = resp.read()
    print("PDF bytes received:", len(content))
    with open("real_fubun_copy.pdf", "wb") as f:
        f.write(content)
        
print("Saved real_fubun_copy.pdf!")
