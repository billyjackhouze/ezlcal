from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("spanBlocks")
while idx >= 0:
    print(idx, repr(html[idx:idx+120]))
    idx = html.find("spanBlocks", idx+1)
