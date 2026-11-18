from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix mdEdge - isLast needs to check endDate===ds not date===ds
# Current: isLast=e.endDate===ds - this is correct
# But multiDay now includes both start AND last day
# On last day (Fri): e.date=Nov17, e.endDate=Nov20, ds=Nov20
# isLast = e.endDate===ds = Nov20===Nov20 = TRUE - correct
# _mdStart should be '00:00', _mdEnd should be e.end='12:00'
# But we're seeing 8:00 AM which means _mdStart is using e.time

# Check the mdEdge definition
idx = html.find("const mdEdge=multiDay.map")
print(repr(html[idx:idx+300]))
