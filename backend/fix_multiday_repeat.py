from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Remove allday banner for multi-day timed events - back to true all-day only
old_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
new_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
if old_allday in html:
    html = html.replace(old_allday, new_allday, 1)
    print("OK: allday true all-day only")

# 2. Add multi-day timed back into timed blocks with per-day height calc
old_timed = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
new_timed = (
    # Regular single-day timed events
    "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
    # Multi-day timed: add as separate entries with adjusted time per segment
    "const mdSpans=evs.filter(e=>e.time&&e.endDate&&e.endDate>e.date&&e.date<=ds&&e.endDate>=ds).map(function(e){"
    "var isFirst=e.date===ds,isLast=e.endDate===ds;"
    "return Object.assign({},e,{"
    # First day: start at event time, end at H1 (top of hour)
    # Middle days: start at H0, end at H1 (full column)  
    # Last day: start at H0, end at event end time
    "_mdStart:isFirst?e.time:(H0+':00'),"
    "_mdEnd:isLast?(e.end||e.time):(H1+':00'),"
    "_mdFirst:isFirst,_mdLast:isLast"
    "});"
    "});"
)
if old_timed in html:
    html = html.replace(old_timed, new_timed, 1)
    print("OK: mdSpans added")

# 3. Update the blocks render to use _mdStart/_mdEnd for multi-day segments
# Find the blocks=timed.map and add mdSpans
old_blocks = "const blocks=timed.map(e=>{"
new_blocks = "const blocks=[...timed,...mdSpans].map(e=>{"
if old_blocks in html:
    html = html.replace(old_blocks, new_blocks, 1)
    print("OK: blocks includes mdSpans")

# 4. Update the toMin calls to use _mdStart/_mdEnd if present
old_tomin = "const s=toMin(e.time),en=e.end?toMin(e.end):s+60;"
new_tomin = "const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;"
if old_tomin in html:
    html = html.replace(old_tomin, new_tomin, 1)
    print("OK: toMin uses _mdStart/_mdEnd")
else:
    print("MISS: toMin - searching")
    idx = html.find("toMin(e.time)")
    print(repr(html[max(0,idx-20):idx+80]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
