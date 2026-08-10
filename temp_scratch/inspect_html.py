import re

with open('page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find all .action strings
actions = re.findall(r'[\w\-\/\!]+\.action', html)
print("Action endpoints found:")
for a in set(actions):
    print("  ", a)

# Find select elements or inputs or tables
print("\nInputs:")
inputs = re.findall(r'<input.*?>', html, re.IGNORECASE)
for inp in inputs:
    print("  ", inp)

print("\nSelects:")
selects = re.findall(r'<select.*?>[\s\S]*?</select>', html, re.IGNORECASE)
for sel in selects:
    print("  ", sel[:200])

print("\nDivs with class or id:")
divs = re.findall(r'<(div|table|iframe|a)\s+[^>]*?(id|class|href)=["\'][^"\']+["\'][^>]*?>', html, re.IGNORECASE)
for d in divs[:30]:
    print("  ", d)
