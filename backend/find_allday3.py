from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find allday in week view - look for the whead allday row
idx = html.find("all-day")
while idx >= 0:
    print(idx, repr(html[max(0,idx-200):idx+200]))
    idx = html.find("all-day", idx+1)
