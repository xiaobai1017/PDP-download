import re

with open('query_jilin_p1.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find pagination info
print("Pagination search:")
page_matches = re.findall(r'.{0,100}共.{0,50}页.{0,100}', html)
for m in page_matches:
    print("Match:", m.strip())

matches2 = re.findall(r'.{0,100}pageNo.{0,100}', html)
for m in matches2:
    print("Match2:", m.strip())

# Search for total count or script variables
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
for s in scripts:
    if 'totalPages' in s or 'total' in s or 'page' in s:
        for line in s.split('\n'):
            if any(k in line for k in ['total', 'count', 'Page', 'page']):
                print("  Script line:", line.strip()[:150])
