from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

idx = html.find('"f_end"')
old = html[idx:idx+80]
new = old.replace('><label', '><input type="date" id="f_end_date" value="${e.endDate||\'\'}" title="End date" aria-label="End date" style="margin-left:4px"><label')
html = html[:idx] + new + html[idx+80:]
print("f_end_date in html:", "f_end_date" in html)
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
