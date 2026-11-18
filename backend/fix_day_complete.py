from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix day view timed filter and add mdSpans
old = "const timed=evs.filter(e=>e.time&&!(e.endDate&&e.endDate>e.date));\n    const spanBlocks='';"
new = ("const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));\n"
       "    const mdSpans=evs.filter(e=>e.time&&e.endDate&&e.endDate>e.date&&e.date<=ds&&e.endDate>=ds).map(function(e){"
       "var isFirst=e.date===ds,isLast=e.endDate===ds;"
       "return Object.assign({},e,{"
       "_mdStart:isFirst?e.time:(H0+':00'),"
       "_mdEnd:isLast?(e.end||e.time):(H1+':00')"
       "});});\n"
       "    const spanBlocks='';")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: day view timed fixed + mdSpans added")
else:
    print("MISS")
    idx = html.find("S.calMode==='day'")
    idx2 = html.find("const timed=", idx)
    print(repr(html[idx2:idx2+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
