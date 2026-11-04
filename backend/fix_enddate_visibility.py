from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove the conditional display:none - always show end date
old = ('id="f_end_date" value="${e.endDate||\'\'}" '
       'title="End date (multi-day)" aria-label="End date">')
new = ('id="f_end_date" value="${e.endDate||\'\'}" '
       'title="End date (multi-day)" placeholder="End date" aria-label="End date">')
if old in html:
    html = html.replace(old, new, 1)
    print("OK: removed style attr")

# Check what style is on it
idx = html.find('id="f_end_date"')
print("f_end_date context:", repr(html[idx:idx+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
