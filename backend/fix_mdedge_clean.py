from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove debug log first
html = html.replace(
    "mdEdge.map(e=>{console.log('mdEdge',e.title,e.date,e.endDate,e._mdStart,e._mdEnd,e.end,e.time);var st=e._mdStart||e.time,et=e._mdEnd||(e.end||'');",
    "mdEdge.map(e=>{var st=e._mdStart||e.time,et=e._mdEnd||(e.end||'');",
    )
print("debug removed:", "console.log" not in html)

# Fix mdEdge definition - explicitly set _mdEnd for last day
old = ("const mdEdge=multiDay.map(function(e){"
       "var isLast=e.endDate===ds;"
       "return Object.assign({},e,{"
       "_mdStart:isLast?'00:00':e.time,"
       "_mdEnd:isLast?(e.end||e.time):'23:59',"
       "_isEdge:true"
       "});});")
new = ("const mdEdge=multiDay.map(function(e){"
       "var isLast=e.endDate===ds;"
       "var mdStart=isLast?'00:00':e.time;"
       "var mdEnd=isLast?(e.end&&e.end!==''?e.end:e.time):'23:59';"
       "return Object.assign({},e,{_mdStart:mdStart,_mdEnd:mdEnd,_isEdge:true});"
       "});")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: mdEdge rewritten")
else:
    print("MISS mdEdge def")
    idx = html.find("const mdEdge=multiDay")
    print(repr(html[idx:idx+200]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
