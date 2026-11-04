from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Restore timed block on start day for multi-day events
old = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
new = "const timed=evs.filter(e=>e.date===ds&&e.time);"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: timed block restored on start day")
else:
    print("MISS")
    idx = html.find("const timed=evs")
    print(repr(html[idx:idx+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
