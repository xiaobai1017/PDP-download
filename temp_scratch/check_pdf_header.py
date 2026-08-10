with open("real_fubun_copy.pdf", "rb") as f:
    header = f.read(10)
    print("Header bytes:", header)
    if header.startswith(b"%PDF"):
        print("CONFIRMED: Valid PDF Document File!")
    else:
        print("Not raw PDF header, starts with:", header)
