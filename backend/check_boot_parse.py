from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find where bootstrap response is parsed
idx = html.find("boot.accounts")
while idx >= 0:
    print(idx, repr(html[max(0,idx-30):idx+100]))
    idx = html.find("boot.accounts", idx+1)
    if idx > 20000: break

# Find the fetch of bootstrap
idx2 = html.find("bootstrap")
while idx2 >= 0:
    chunk = html[max(0,idx2-20):idx2+80]
    if "fetch" in chunk or "api" in chunk.lower():
        print("fetch:", repr(chunk))
    idx2 = html.find("bootstrap", idx2+1)
    if idx2 > 30000: break
