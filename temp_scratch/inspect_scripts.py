import re

with open('page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find all script blocks
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
print(f"Total script blocks: {len(scripts)}")

for i, s in enumerate(scripts):
    if len(s.strip()) > 0:
        print(f"--- Script {i} (len: {len(s)}) ---")
        lines = [line for line in s.split('\n') if any(k in line for k in ['action', 'post', 'get', 'ajax', 'url', 'search', 'page', 'province', '吉林', 'xzkx', 'permit', 'select', 'table', 'data'])]
        for l in lines[:30]:
            print("  ", l.strip()[:150])
