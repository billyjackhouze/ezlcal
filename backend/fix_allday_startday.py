from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Check current allday filter
idx = html.find("e.date<=ds&&(e.endDate||e.date)>=ds")
print(repr(html[idx:idx+120]))

# The issue: on start day, e.date===ds is true so !==ds is false - should NOT show
# But it IS showing - likely the filter has e.date!==ds wrong
# Fix: explicitly only show on days AFTER start date
old = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||(e.endDate&&e.endDate>e.date&&e.date!==ds))).map"
new = "evs.filter(e=>e.date<ds&&(e.endDate||e.date)>=ds&&(!e.time||(e.endDate&&e.endDate>e.date))||e.date===ds&&!e.time).map"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: allday - continuation days use e.date<ds")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
