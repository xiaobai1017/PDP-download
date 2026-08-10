import re

with open('detail_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print("Searching for pdf, 排污许可证, download, onclick, href in detail_page.html...")

# Find all a tags or buttons or inputs with href or onclick
links = re.findall(r'<a[\s\S]*?>[\s\S]*?</a>', html, re.IGNORECASE)
print(f"Links found: {len(links)}")
for l in links:
    if any(k in l for k in ['副本', '正本', 'pdf', 'PDF', 'download', 'xkgk', 'file', 'down']):
        print("LINK:", l.strip())

# Find all javascript functions
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', html, re.IGNORECASE)
for s in scripts:
    if any(k in s for k in ['pdf', 'PDF', 'down', 'fb', 'zb', 'xkgkAction', 'getxxgkContent', 'open']):
        print("SCRIPT:")
        for line in s.split('\n'):
            if line.strip():
                print("  ", line.strip())
