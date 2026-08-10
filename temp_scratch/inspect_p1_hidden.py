import re

with open('query_jilin_p1.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find all hidden inputs or inputs inside mainForm
inputs = re.findall(r'<input[^>]*?>', html, re.IGNORECASE)
print("All inputs in query_jilin_p1.html:")
for inp in inputs:
    print("  ", inp)

# Check page info in query_jilin_p1.html
matches = re.findall(r'id=["\']pageNo["\'][^>]*', html)
print("\npageNo element:", matches)
