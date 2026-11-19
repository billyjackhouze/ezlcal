from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix day view mdEdge.map at 49933 - same fixes as week view
old = ("mdEdge.map(e=>{const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;"
       "const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);"
       "return '<button class=\"blk\" data-open=\"'+esc(e.id)+'\" style=\"top:'+top+'px;height:'+h+'px;"
       "left:1px;width:calc(100% - 2px);background:'+staffColor(e")
new = ("mdEdge.map(e=>{var st=e._mdStart||e.time,et=e._mdEnd||(e.end||'');var s=toMin(st),en=et?toMin(et):s+60;if(en<=s)en=s+60;"
       "const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);"
       "return '<button class=\"blk\" data-open=\"'+esc(e.id)+'\" style=\"top:'+top+'px;height:'+h+'px;"
       "left:1px;width:calc(60% - 2px);background:'+staffColor(e")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: day view mdEdge fixed")
else:
    print("MISS")
    idx = html.find("mdEdge.map(e=>{const")
    print(repr(html[idx:idx+150]))

# Also fix the label in day view mdEdge
old_label = ("+';opacity:.85;z-index:1\">'+"
             "'<b>'+(e.endDate===ds?'→ '+fmtTime(e._mdEnd):fmtTime(e.time))+'</b> '+esc(e.title)+'</button>';")
new_label = ("+';opacity:.85;z-index:1\">'+"
             "'<b>'+(e.endDate===ds?'→ '+fmtTime(e._mdEnd):fmtTime(e._mdStart||e.time))+'</b> '+esc(e.title)+'</button>';")
if old_label in html:
    html = html.replace(old_label, new_label, 1)
    print("OK: day view label fixed")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
