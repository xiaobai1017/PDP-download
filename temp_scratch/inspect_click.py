import re

with open('page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print("Searching for licenseInformation in page.html...")
matches = re.findall(r'.{0,150}licenseInformation.{0,150}', html)
for m in matches:
    print("Match:", m.strip())
