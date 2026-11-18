from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find ALL allday filter occurrences
idx = 0
while True:
    idx = html.find("e.date<=ds&&(e.endDate||e.date)>=ds", idx)
    if idx < 0: break
    print(idx, repr(html[idx:idx+100]))
    idx += 1
