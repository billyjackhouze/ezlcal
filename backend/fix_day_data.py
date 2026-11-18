from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find all calMode==='day' occurrences
idx = 0
while True:
    idx = html.find("calMode==='day'", idx)
    if idx < 0: break
    print(idx, repr(html[max(0,idx-30):idx+80]))
    idx += 1
