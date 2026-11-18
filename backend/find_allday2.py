from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the week allday row rendering
idx = html.find("adb")
while idx >= 0:
    chunk = html[max(0,idx-100):idx+100]
    if "filter" in chunk or "allday" in chunk.lower() or "all-day" in chunk.lower():
        print(idx, repr(chunk))
    idx = html.find('"adb"', idx+1)
    if idx > 60000: break
