with open("real_fubun_copy.pdf", "rb") as f:
    data = f.read()

print("Total length:", len(data))
print("First 200 bytes raw:", data[:200])

# Strip leading BOM or whitespace
stripped = data.lstrip(b'\xef\xbb\xbf\r\n\t ')
print("First 100 bytes after stripping whitespace/BOM:", stripped[:100])

if stripped.startswith(b"%PDF"):
    print("MATCH! It is a PDF document wrapped with leading BOM/whitespace.")
    # Save clean pdf
    with open("clean_fubun_copy.pdf", "wb") as f_out:
        f_out.write(stripped)
    print("Saved clean_fubun_copy.pdf")
else:
    print("First 500 chars as text:", stripped[:500].decode('utf-8', errors='ignore'))
