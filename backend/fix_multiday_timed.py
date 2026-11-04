from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Week view: timed events in allday row for days after start
# Current allday filter: date<=ds && endDate>=ds && !time
# For timed multi-day: show in allday row on days AFTER the start date
old = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.date<ds)).map"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: week allday shows timed multi-day on continuation days")
else:
    print("MISS - checking...")
    idx = html.find("allday")
    print(repr(html[idx:idx+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
