from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Separate mdEdge from timed in allTimed - render edge blocks independently
old = "const mdSpans=[];const allTimed=[...timed,...mdEdge];"
new = "const mdSpans=[];const allTimed=timed;"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: allTimed=timed only")

# Add mdEdge blocks to the template separately (full width, behind other blocks)
old_dcol = "${blocks}${spanBlocks}${nowl}</div></div>`;"
new_dcol = ("${mdEdge.map(e=>{const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;"
            "const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);"
            "return '<button class=\"blk\" data-open=\"'+esc(e.id)+'\" style=\"top:'+top+'px;height:'+h+'px;"
            "left:1px;width:calc(100% - 2px);background:'+staffColor(e)+';opacity:.85;z-index:1\">"
            "<b>'+(e._isEdge&&e.endDate===ds?'→ ends '+fmtTime(e._mdEnd):fmtTime(e.time))+'</b> '+esc(e.title)+'</button>';"
            "}).join('')}${blocks}${spanBlocks}${nowl}</div></div>`;")
if old_dcol in html:
    html = html.replace(old_dcol, new_dcol, 1)
    print("OK: mdEdge rendered full-width behind blocks")
else:
    print("MISS dcol")
    idx = html.find("${blocks}${spanBlocks}")
    print(repr(html[max(0,idx-20):idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
