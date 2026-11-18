from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove mdSpans from blocks entirely - keep only start day timed block
# Replace [...timed,...mdSpans] with just timed
old = "const blocks=[...timed,...mdSpans].map(e=>{"
new = "const blocks=timed.map(e=>{"
count = html.count(old)
print(f"Found {count} occurrences of blocks")
html = html.replace(old, new)

# Remove mdSpans definitions (both week and day view)
html = re.sub(
    r"const mdSpans=evs\.filter\(e=>e\.time&&e\.endDate&&e\.endDate>e\.date&&e\.date<=ds&&e\.endDate>=ds\)[\s\S]*?\}\);\}\);",
    "const mdSpans=[];",
    html
)
print("mdSpans cleared:", "mdSpans=[];" in html)

# Start day: show timed block from start time to bottom of grid (tall block)
# already handled by timed filter - just need to restore the tall block for start day
old_timed = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
new_timed = "const timed=evs.filter(e=>e.date===ds&&e.time);"
count2 = html.count(old_timed)
print(f"Found {count2} timed filters")
html = html.replace(old_timed, new_timed)

# All-day banner for multi-day events on continuation days only (not start day)
old_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||(e.endDate&&e.endDate>e.date&&e.date!==ds))).map"
if old_allday in html:
    html = html.replace(old_allday, new_allday, 1)
    print("OK: allday shows banner on continuation days only")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
