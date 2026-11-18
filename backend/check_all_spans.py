from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print("=== spanBlocks ===")
idx = 0
while True:
    idx = html.find("spanBlocks", idx)
    if idx < 0: break
    print(idx, repr(html[max(0,idx-20):idx+100]))
    idx += 1
print("=== multiDay ===")
idx = 0
while True:
    idx = html.find("multiDay", idx)
    if idx < 0: break
    print(idx, repr(html[max(0,idx-20):idx+100]))
    idx += 1
