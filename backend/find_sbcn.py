from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = 0
while True:
    i = html.find("staffColorByName", idx)
    if i < 0: break
    print(f"At {i}: {repr(html[max(0,i-30):i+60])}")
    idx = i+1
