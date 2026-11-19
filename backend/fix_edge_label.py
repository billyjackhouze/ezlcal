from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix start day label - should show actual start time, not _mdStart (which is e.time anyway for start day)
# The issue: fmtTime(e.time) is correct for start day
# But we see "8:00 AM" - check what fmtTime does with e.time vs e._mdStart
# For start day: _mdStart=e.time, _mdEnd='23:59', isLast=false
# For last day: _mdStart='00:00', _mdEnd=e.end, isLast=true (endDate===ds)
# Label logic: start day -> show start time, last day -> show "-> end time"
# Current: (e.endDate===ds?"→ "+fmtTime(e._mdEnd):fmtTime(e.time))
# That should be correct... unless e.time is empty on start day somehow

# Check - add start time to label for debugging
old = '+"<b>"+(e.endDate===ds?"→ "+fmtTime(e._mdEnd):fmtTime(e.time))+"</b> "+esc(e.title)+"</button>";'
new = '+"<b>"+(e.endDate===ds?"→ "+fmtTime(e._mdEnd):fmtTime(e._mdStart||e.time))+"</b> "+esc(e.title)+"</button>";'
count = html.count(old)
print(f"Found {count}")
html = html.replace(old, new)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
