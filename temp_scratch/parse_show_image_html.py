import re

with open("showImage_result.html_or_pdf", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Find iframe, pdf, embed, object, img, href, or script tags
print("Searching elements in showImage HTML:")
for tag in ['iframe', 'embed', 'object', 'a', 'img', 'script']:
    matches = re.findall(rf'<{tag}[\s\S]*?>', html, re.IGNORECASE)
    if matches:
        print(f"--- Tag <{tag}> ({len(matches)}) ---")
        for m in matches[:10]:
            print("  ", m.strip()[:200])

# Search for pdf or download links
links = re.findall(r'[\w\-\/\!\.]+\.(?:pdf|action)[^\s"\']*', html, re.IGNORECASE)
print("\nPDF / Action URLs found in page:")
for l in set(links):
    print("  ", l)
