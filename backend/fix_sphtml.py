from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find _sphtml definition
idx = html.find("_sphtml")
while idx >= 0:
    print(idx, repr(html[max(0,idx-20):idx+100]))
    idx = html.find("_sphtml", idx+1)
