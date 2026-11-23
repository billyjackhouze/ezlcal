from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("linkBy")
while idx >= 0:
    print(idx, repr(html[max(0,idx-20):idx+100]))
    idx = html.find("linkBy", idx+1)
    if idx > 25000: break
