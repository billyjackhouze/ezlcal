from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print("size:", len(html))
idx = html.find("const timed=")
print("timed at:", idx, repr(html[idx:idx+150]))
idx2 = html.find("spanBlocks")
print("spanBlocks at:", idx2, repr(html[idx2:idx2+150]))
