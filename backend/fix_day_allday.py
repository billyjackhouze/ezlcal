from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find day view allDay definition
idx = html.find("const allDay=evs.filter")
print("allDay filter:", repr(html[idx:idx+100]))

# Fix: allDay in day view should only show true all-day events (no time)
old = "const allDay=evs.filter(e=>!e.time);"
new = "const allDay=evs.filter(e=>!e.time&&!(e.endDate&&e.endDate>e.date));"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: day view allDay fixed")
else:
    print("MISS - current:", repr(html[idx:idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
