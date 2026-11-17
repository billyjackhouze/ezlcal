from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Remove spanBlocks from timed area - replace with empty string
import re
html = re.sub(r"const spanBlocks=evs\.filter[^;]+;", "const spanBlocks='';", html, count=1)
print("spanBlocks cleared:", "const spanBlocks='';" in html)

# 2. Put multi-day timed events in all-day row
old = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: multi-day in all-day row")
else:
    print("already set")

# 3. Restore timed filter
old2 = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
if old2 in html:
    html = html.replace(old2, "const timed=evs.filter(e=>e.date===ds&&e.time);", 1)
    print("OK: timed restored")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
