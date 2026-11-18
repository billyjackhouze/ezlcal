from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix lanes to use _mdStart and blocks to use _mdStart/_mdEnd
old = ("const lanes=[];allTimed.forEach(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;"
       "let L=0;while(lanes[L]&&lanes[L]>s)L++;lanes[L]=en;e._l=L;});")
new = ("const lanes=[];allTimed.forEach(e=>{const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;"
       "let L=0;while(lanes[L]&&lanes[L]>s)L++;lanes[L]=en;e._l=L;});")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: lanes use _mdStart/_mdEnd")
else:
    print("MISS lanes")
    idx = html.find("const lanes=[];allTimed")
    print(repr(html[idx:idx+120]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
