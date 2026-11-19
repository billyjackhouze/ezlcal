from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = '${blocks}${nowl}</div>`;}).join'
new = ('${mdEdge.map(e=>{var s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||""))||s+60;'
       'var top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);'
       'return "<button class=\\"blk\\" data-open=\\""+esc(e.id)+"\\" style=\\"top:"+top+"px;height:"+h+"px;'
       'left:1px;width:calc(100% - 2px);background:"+staffColor(e)+";opacity:.9;z-index:1\\">"'
       '+"<b>"+(e.endDate===ds?"→ "+fmtTime(e._mdEnd):fmtTime(e.time))+"</b> "+esc(e.title)+"</button>";'
       '}).join("")}${blocks}${nowl}</div>`;}).join')

if old in html:
    html = html.replace(old, new, 1)
    print("OK: mdEdge in week dcol")
else:
    print("MISS")
    idx = html.find("${blocks}${nowl}")
    print(repr(html[idx:idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
