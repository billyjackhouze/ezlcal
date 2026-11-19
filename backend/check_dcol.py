from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("${blocks}${spanBlocks}")
print(repr(html[max(0,idx-20):idx+100]))
idx2 = html.find("mdEdge.map")
print("mdEdge.map:", idx2, repr(html[idx2:idx2+80]) if idx2>=0 else "not found")
