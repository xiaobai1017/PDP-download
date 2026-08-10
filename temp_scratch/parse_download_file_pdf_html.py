with open("real_fubun_copy.pdf", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re
print("HTML length:", len(html))

# Find iframe, pdf, embed, object, img, href, or script tags
for tag in ['iframe', 'embed', 'object', 'a', 'img', 'script']:
    matches = re.findall(rf'<{tag}[\s\S]*?>', html, re.IGNORECASE)
    if matches:
        print(f"--- Tag <{tag}> ({len(matches)}) ---")
        for m in matches[:10]:
            print("  ", m.strip()[:200])

print("\n--- Searching for pdf / download / show / file in html ---")
matches = re.findall(r'.{0,100}(?:pdf|down|file|show|image|src).{0,100}', html, re.IGNORECASE)
for m in matches[:30]:
    if any(k in m for k in ['.action', '.pdf', '.png', '.jpg', 'src=']):
        print("Match:", m.strip()[:150])
