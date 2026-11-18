from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find all references to multiDay
idx = 0
while True:
    idx = html.find("multiDay", idx)
    if idx < 0: break
    print(idx, repr(html[max(0,idx-30):idx+80]))
    idx += 1
# Find blocks render
idx2 = html.find("const blocks=")
while idx2 >= 0:
    print("blocks:", repr(html[idx2:idx2+80]))
    idx2 = html.find("const blocks=", idx2+1)
    if idx2 > 55000: break
