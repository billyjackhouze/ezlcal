from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find week timed filter
idx = html.find("const multiDay=evs.filter")
print(repr(html[idx:idx+300]))

# Add start day and last day blocks after timed
old = "const multiDay=evs.filter(e=>e.date===ds&&e.time&&e.endDate&&e.endDate>e.date);const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));const mdSpans=[];const allTimed=timed;"
new = ("const multiDay=evs.filter(e=>e.date===ds&&e.time&&e.endDate&&e.endDate>e.date);"
       "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
       # Start day block: from start time to end of grid
       # Last day block: from start of grid to end time
       "const mdEdge=multiDay.map(function(e){"
       "var isLast=e.endDate===ds;"
       "return Object.assign({},e,{"
       "_mdStart:isLast?'00:00':e.time,"
       "_mdEnd:isLast?(e.end||e.time):'23:59',"
       "_isEdge:true"
       "});});"
       "const mdSpans=[];const allTimed=[...timed,...mdEdge];")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: mdEdge added for start/end days")
else:
    print("MISS")

# Update blocks render to use _mdStart/_mdEnd for edge blocks
old_blocks = "const blocks=timed.map(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;"
new_blocks = "const blocks=allTimed.map(e=>{const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;"
if old_blocks in html:
    html = html.replace(old_blocks, new_blocks, 1)
    print("OK: blocks uses allTimed with _mdStart/_mdEnd")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
