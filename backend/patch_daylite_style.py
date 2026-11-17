from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and replace the entire timed+spanBlocks section
start = html.find("const timed=evs.filter(e=>e.date===ds&&e.time);const spanBlocks=")
if start < 0:
    start = html.find("const timed=evs.filter(e=>e.date===ds&&e.time);")
    print("timed found at:", start)
    idx2 = html.find("spanBlocks", start)
    print("spanBlocks at:", idx2, repr(html[idx2:idx2+80]))
else:
    end = html.find(".join('');", start) + len(".join('');")
    print(f"Replacing {end-start} chars at {start}")
    new_block = (
        "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
        "const spanBlocks=evs.filter(e=>e.time&&e.endDate&&e.endDate>e.date&&e.date===ds).map(function(e){"
        "var s=toMin(e.time);"
        "var top=Math.max(0,(s-H0*60))*48/60;"
        "var h=(H1-H0)*48-top;"
        "return '<button class=\"blk\" data-open=\"'+esc(e.id)+'\" style=\"'"
        "+'top:'+top+'px;height:'+h+'px;left:1px;width:calc(100% - 2px);'"
        "+'background:'+staffColor(e)+';border-radius:4px;z-index:2;overflow:hidden\">'"
        "+'<b>'+fmtTime(e.time)+'</b> '+esc(e.title)+'</button>';"
        "}).join('');"
    )
    html = html[:start] + new_block + html[end:]
    print("OK")

# Also fix allday row - true all-day only
old_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
new_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
if old_allday in html:
    html = html.replace(old_allday, new_allday, 1)
    print("OK: allday fixed")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
