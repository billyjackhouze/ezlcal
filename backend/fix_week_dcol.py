from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find ALL dcol closing patterns
idx = 0
while True:
    idx = html.find("${blocks}${spanBlocks}${nowl}</div></div>", idx)
    if idx < 0: break
    print(idx, repr(html[max(0,idx-50):idx+80]))
    idx += 1
