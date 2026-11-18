from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = ("e===ds&&e.time&&e.endDate&&e.endDate>e.date);const timed=evs.filter(e=>e.date===ds&&e.time);const mdSpans=[];const allTimed=[...timed,...multiDay];\n"
       "      const lanes=[];allTimed.forEach(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;let L=0;while(lanes[L]&&lanes[L]>s)L++;lanes[L]=en;e._l=L;});")
new = ("e===ds&&e.time&&e.endDate&&e.endDate>e.date);const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));const mdSpans=[];const allTimed=timed;\n"
      "      const lanes=[];allTimed.forEach(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;let L=0;while(lanes[L]&&lanes[L]>s)L++;lanes[L]=en;e._l=L;});")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: removed multiDay from allTimed")
else:
    print("MISS")
    idx = html.find("allTimed=")
    print(repr(html[max(0,idx-50):idx+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
