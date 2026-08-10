import re

with open('license_info.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Inspect form elements
form_match = re.search(r'<form id="mainForm"[\s\S]*?</form>', html)
if form_match:
    form_html = form_match.group(0)
    print("--- Inputs and Selects inside mainForm ---")
    inputs = re.findall(r'<(input|select|button)[\s\S]*?>', form_html)
    for inp in inputs:
        print(inp)
        
    print("\n--- Full Form HTML snippet ---")
    print(form_html[:3000])

# Inspect scripts for getProvinces, getCitys, search, page function, view function
print("\n--- Script Details ---")
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
for s in scripts:
    if 'getProvinces' in s or 'search' in s or 'detail' in s or 'view' in s or 'xkgg!' in s:
        print(s)
        print("="*60)
