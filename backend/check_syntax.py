from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the broken area - mdEdge at ~49933
idx = html.find("mdEdge")
while idx >= 0 and idx < 51000:
    print(idx, repr(html[max(0,idx-30):idx+80]))
    idx = html.find("mdEdge", idx+1)
