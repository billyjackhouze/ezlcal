from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find map rendering code
idx = html.find("office_type")
while idx >= 0:
    print(repr(html[max(0,idx-30):idx+80]))
    idx = html.find("office_type", idx+1)
    if idx > 0 and html.count("office_type") > 10:
        break
