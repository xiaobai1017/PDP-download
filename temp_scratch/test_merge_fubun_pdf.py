import urllib.request, ssl, re, io
from PIL import Image

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dataid = "500bbe89c72f4691bb45e1f5adac37b9"
show_image_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid={dataid}"
INIT_URL = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"

print(f"Fetching showImage page: {show_image_url}...")
req = urllib.request.Request(
    show_image_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": INIT_URL
    }
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Extract imgCount, pkid, dataid
img_count_m = re.search(r'id="imgCount"\s+value="(\d+)"', html)
pkid_m = re.search(r'id="pkid"\s+value="([^"]+)"', html)

img_count = int(img_count_m.group(1)) if img_count_m else 0
pkid = pkid_m.group(1) if pkid_m else ""

print(f"Found imgCount: {img_count}, pkid: {pkid}")

if img_count > 0 and pkid:
    pil_images = []
    # Test fetching first 3 pages as demonstration
    test_pages = min(3, img_count)
    print(f"Downloading first {test_pages} pages of 副本...")
    for i in range(1, test_pages + 1):
        img_url = f"https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!downFilePng.action?datafileid={pkid}_{i}&fileType=pdffile&dataid={dataid}"
        req_img = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0", "Referer": show_image_url})
        with urllib.request.urlopen(req_img, context=ctx, timeout=15) as r_img:
            img_bytes = r_img.read()
            print(f"  Page {i}/{img_count}: {len(img_bytes)} bytes")
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            pil_images.append(img)
            
    if pil_images:
        pdf_out = "首都医科大学附属北京安贞医院吉林医院_排污许可证副本.pdf"
        pil_images[0].save(pdf_out, "PDF", resolution=100.0, save_all=True, append_images=pil_images[1:])
        print(f"\nSUCCESS! Merged into PDF: {pdf_out}")
