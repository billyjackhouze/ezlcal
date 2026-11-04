from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Week view: treat multi-day timed events as allday on ALL days (including start)
# Change: show in allday row if endDate > date (not just continuation days)
old = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.date<ds)).map"
new = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: allday row shows all days of multi-day event")

# Also hide the timed block on start day when event spans multiple days
old_timed = "const timed=evs.filter(e=>e.date===ds&&e.time);"
new_timed = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
if old_timed in html:
    html = html.replace(old_timed, new_timed, 1)
    print("OK: timed block hidden when multi-day")
else:
    print("MISS timed filter - searching...")
    idx = html.find("const timed=evs")
    print(repr(html[idx:idx+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
