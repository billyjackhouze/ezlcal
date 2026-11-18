from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = "    const evs=(EZ.evs||[]).filter(e=>e.date===ds);"
new = "    const evs=calEvents().filter(e=>e.date===ds);"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: calEvents() in day view")
else:
    print("MISS")
    idx = html.find("EZ.evs||[]")
    print(repr(html[max(0,idx-20):idx+80]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
