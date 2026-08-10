import re

with open('page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Search for perxxgkinfo or licenseInformation
matches = re.findall(r'.{0,100}licenseInformation.{0,100}', html)
for m in matches:
    print("Match:", m.strip())

print("--- Searching for perxxgkinfo ---")
matches2 = re.findall(r'.{0,100}perxxgkinfo.{0,100}', html)
for m in matches2[:10]:
    print("Match2:", m.strip())
