import csv

with open('downloads_manifest.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"P{row['page']}-{row['index']} | {row['company_name']} | {row['xkz_num']} | {row['status']} | {row['pdf_filename']}")
