from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix multiDay filter to include BOTH start day AND last day
old = "const multiDay=evs.filter(e=>e.date===ds&&e.time&&e.endDate&&e.endDate>e.date);"
new = "const multiDay=evs.filter(e=>e.time&&e.endDate&&e.endDate>e.date&&(e.date===ds||e.endDate===ds));"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: multiDay includes last day")
else:
    print("MISS")
    idx = html.find("const multiDay=")
    print(repr(html[idx:idx+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
