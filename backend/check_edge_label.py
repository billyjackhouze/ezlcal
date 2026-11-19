from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("mdEdge.map")
while idx >= 0:
    print(idx, repr(html[idx:idx+300]))
    idx = html.find("mdEdge.map", idx+1)
