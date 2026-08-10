import re

with open('license_info.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print("Length:", len(html))

# Find forms
forms = re.findall(r'<form[\s\S]*?</form>', html, re.IGNORECASE)
print(f"Forms found: {len(forms)}")
for i, form in enumerate(forms):
    print(f"--- Form {i} ---")
    print(form[:500])

# Find script tags
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
print(f"\nScripts found: {len(scripts)}")
for i, s in enumerate(scripts):
    if any(k in s for k in ['search', 'submit', 'post', 'ajax', 'page', 'province', '吉林', 'xzkx', 'open', 'detail', 'view', 'href', 'location', 'action']):
        print(f"--- Script {i} ---")
        lines = [line.strip() for line in s.split('\n') if line.strip()]
        for l in lines[:30]:
            print("  ", l[:150])
