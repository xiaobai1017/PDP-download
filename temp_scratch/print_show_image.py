import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("showImage_result.html_or_pdf", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    print(f"{i+1:03d}: {l.rstrip()}")
