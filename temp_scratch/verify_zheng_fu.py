import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("detail_page.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re

matches = re.findall(r'<a[^>]*?>[\s\S]*?</a>', html, re.IGNORECASE)
for i, m in enumerate(matches[:3]):
    print(f"--- Link {i+1} ---")
    print(m)
