from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Remove all-day banners for multi-day timed events
old_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&(!e.time||e.endDate>e.date)).map"
new_allday = "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map"
if old_allday in html:
    html = html.replace(old_allday, new_allday, 1)
    print("OK: allday row - true all-day only")
else:
    print("allday already fixed")

# 2. Fix span positioning to use calc() with 56px time col
idx = html.find("_left=(_d1+1)/(_N+1)*100;")
if idx >= 0:
    end = html.find("+'</button>';", idx) + len("+'</button>';")
    new_span = (
        "_left='calc(56px + '+_d1+' * ((100% - 56px) / '+_N+'))';\n"
        "    var _wid='calc('+_nd+' * ((100% - 56px) / '+_N+') - 4px)';\n"
        "    _sphtml+='<button class=\"blk span-blk\" data-open=\"'+esc(e.id)+'\" style=\"'\n"
        "      +'top:'+_top+'px;height:'+_h+'px;'\n"
        "      +'left:'+_left+';width:'+_wid+';'\n"
        "      +'background:'+staffColor(e)+';z-index:3;pointer-events:auto'>'\n"
        "      +'<b>'+fmtTime(e.time)+'</b> '+esc(e.title)\n"
        "      +'</button>';"
    )
    html = html[:idx] + new_span + html[end:]
    print("OK: calc() positioning")
else:
    print("span positioning already fixed or not found")
    idx2 = html.find("_left=")
    print(repr(html[idx2:idx2+80]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
