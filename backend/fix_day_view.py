from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = "    const evs=EZ.evs.filter(e=>e.date===ds);"
new = "    const evs=(EZ.evs||[]).filter(e=>e.date===ds);"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: evs null guard")
else:
    print("MISS")
    idx = html.find("EZ.evs.filter")
    print(repr(html[idx:idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
