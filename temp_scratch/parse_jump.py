import re

with open('license_info.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Search for jumpPage or gojumpPage or pageNo
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
for s in scripts:
    if 'jumpPage' in s or 'gojumpPage' in s:
        print("FOUND SCRIPT:")
        print(s)
