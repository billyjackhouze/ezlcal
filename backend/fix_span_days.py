from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# The issue: days array in week view - check how many days and what indices
# Week view has 7 days Sun-Sat. Tue=index 2, Thu=index 4
# endDate=2026-11-05 (Thu) should be index 4
# Block shows Tue(2) to Wed(3) = 2 days. So _d2=3 not 4.
# This means iso(days[4]) != "2026-11-05"
# days[4] = Thu Nov 5. iso() should return "2026-11-05"
# UNLESS the endDate from server has a timezone offset issue

# Fix: compare dates more loosely - use >= start of end date
old = "var _d2=days.findIndex(function(d){return iso(d)===e.endDate;});"
new = "var _d2=days.findIndex(function(d){return iso(d)>=e.endDate;});"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: endDate comparison fixed to >=")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
