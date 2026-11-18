from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find allday filter
idx = html.find("evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds")
print("allday filter:", repr(html[idx:idx+120]))

# The allday row should ONLY show events with no time (true all-day)
# AND exclude multi-day timed events (they show in timed columns now)
old = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time&&!(e.time&&e.endDate&&e.endDate>e.date)).map"
# Simpler: just !e.time is already correct - multi-day timed have e.time set
# Check if there is still the (!e.time||e.endDate>e.date) version
old2 = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
if old2 in html:
    html = html.replace(old2, old, 1)
    print("OK: reverted to !e.time only")
elif old in html:
    print("Already !e.time only - bar must be from allDay events, not timed")
    # Check the month view allday filter too
    idx2 = html.find("allDay=evs.filter")
    print("allDay filter:", repr(html[idx2:idx2+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
