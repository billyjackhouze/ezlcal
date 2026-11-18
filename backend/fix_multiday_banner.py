from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Remove spanBlocks entirely
html = re.sub(r"const spanBlocks=evs\.filter\(e=>e\.time&&e\.endDate&&e\.endDate>e\.date&&e\.date===ds\)[\s\S]*?\.join\(''\);", "const spanBlocks='';", html, count=1)
print("spanBlocks removed:", "spanBlocks=evs.filter" not in html)

# 2. Allday row includes multi-day timed events
old_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
if old_allday in html:
    html = html.replace(old_allday, new_allday, 1)
    print("OK: allday includes multi-day timed")
else:
    print("allday already set")

# 3. Exclude multi-day from timed blocks
old_timed = "const timed=evs.filter(e=>e.date===ds&&e.time);"
new_timed = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
if old_timed in html:
    html = html.replace(old_timed, new_timed, 1)
    print("OK: timed excludes multi-day")
else:
    print("timed already set")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
