import re

with open("detail_page.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("HTML Length:", len(html))

# Search for all <a> tags in detail_page.html
matches = re.findall(r'<a[^>]*?>[\s\S]*?</a>', html, re.IGNORECASE)
print(f"Total <a> tags: {len(matches)}")
for i, m in enumerate(matches):
    clean_text = re.sub(r'<[^>]+>', '', m).strip()
    href_m = re.search(r'href=["\']([^"\']+)["\']', m, re.IGNORECASE)
    href = href_m.group(1) if href_m else ''
    print(f"[{i+1}] Text: '{clean_text}' | Href: {href}")

# Search for all "排污许可证" occurrences in detail_page.html
print("\n--- All '排污许可证' occurrences ---")
occ = re.findall(r'.{0,100}排污许可证.{0,100}', html)
for o in occ:
    print("Match:", o.strip())
