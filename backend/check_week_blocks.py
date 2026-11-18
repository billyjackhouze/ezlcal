from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find blocks render in week view
idx = html.find("const blocks=[...timed,...mdSpans]")
if idx < 0: idx = html.find("const blocks=timed.map")
print("blocks at:", idx, repr(html[idx:idx+200]))
# Find the toMin line
idx2 = html.find("toMin(e._mdStart||e.time)")
if idx2 < 0: idx2 = html.find("const s=toMin")
print("toMin at:", idx2, repr(html[idx2:idx2+80]))
