import os, socket

print("HTTP_PROXY env:", os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy"))
print("HTTPS_PROXY env:", os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))

# Check common proxy ports
ports = [7890, 7897, 10809, 1080, 8080]
for p in ports:
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(('127.0.0.1', p))
        print(f"Local proxy port open on 127.0.0.1:{p}")
    except:
        pass
    finally:
        s.close()
