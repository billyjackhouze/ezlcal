from pathlib import Path, re
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Check state
print("spanBlocks empty:", "const spanBlocks='';" in html)
print("spanBlocks filter:", "spanBlocks=evs.filter" in html)
idx = html.find("const timed=evs.filter")
print("timed filter:", repr(html[idx:idx+100]))

# 1. Remove ALL spanBlocks code
html = re.sub(r"const spanBlocks=evs\.filter[\s\S]*?\.join\(''\);", "const spanBlocks='';", html, count=1)
html = re.sub(r"const spanBlocks='';", "const spanBlocks='';", html, count=1)
print("After fix - spanBlocks filter:", "spanBlocks=evs.filter" in html)

# 2. Exclude multi-day from timed area
old = "const timed=evs.filter(e=>e.date===ds&&e.time);"
new = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: multi-day excluded from timed")

# 3. All-day row includes multi-day timed
old2 = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
new2 = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: allday includes multi-day timed")
else:
    print("allday already set")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
