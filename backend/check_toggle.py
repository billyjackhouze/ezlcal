from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find toggle function
idx = html.find("function toggleQJDetail")
print("Toggle fn:", repr(html[idx:idx+200]))

# Find qjdetail CSS
idx2 = html.find("qjdetail")
while idx2 >= 0:
    chunk = html[max(0,idx2-10):idx2+80]
    if "display" in chunk or "style" in chunk or "{" in chunk:
        print(idx2, repr(chunk))
    idx2 = html.find("qjdetail", idx2+1)
    if idx2 > 10000: break
