from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Add console.log to debug mdEdge on last day
old = "mdEdge.map(e=>{var st=e._mdStart||e.time,et=e._mdEnd||(e.end||'');"
new = "mdEdge.map(e=>{console.log('mdEdge',e.title,e.date,e.endDate,e._mdStart,e._mdEnd,e.end,e.time);var st=e._mdStart||e.time,et=e._mdEnd||(e.end||'');"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: debug added")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
