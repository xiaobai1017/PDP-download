import re

with open('query_jilin_p1.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find tables in query_jilin_p1.html
tables = re.findall(r'<table[\s\S]*?</table>', html, re.IGNORECASE)
print(f"Tables found: {len(tables)}")

for i, t in enumerate(tables):
    print(f"=== Table {i} ===")
    rows = re.findall(r'<tr[\s\S]*?</tr>', t, re.IGNORECASE)
    print(f"Rows count: {len(rows)}")
    for j, r in enumerate(rows[:10]):
        # Strip html tags to see text content
        clean_row = re.sub(r'<[^>]+>', ' ', r)
        clean_row = ' '.join(clean_row.split())
        print(f" Row {j}: {clean_row}")
        
        # Check onclick or href in row
        links = re.findall(r'(href=["\'][^"\']+["\']|onclick=["\'][^"\']+["\'])', r, re.IGNORECASE)
        if links:
            print(f"   Links: {links}")
