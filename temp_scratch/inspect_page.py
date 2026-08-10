import re

with open('page.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Length:', len(html))
print('Title:', re.findall(r'<title>(.*?)</title>', html, re.IGNORECASE))
print('Iframes:', re.findall(r'<iframe.*?>', html, re.IGNORECASE))

srcs = re.findall(r'src=["\'](.*?)["\']', html, re.IGNORECASE)
for s in srcs[:20]:
    print('SRC:', s)

if '吉林' in html:
    print("Found '吉林' in page!")
else:
    print("'吉林' not in page html directly.")
