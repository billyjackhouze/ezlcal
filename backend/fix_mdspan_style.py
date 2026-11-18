from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Add visual distinction to mdSpan blocks vs regular blocks
# In the blocks.map, detect _mdStart and style differently
old = ("      const w=100/n;\n"
       "        return `<button class=\"blk\" data-open=\"${esc(e.id)}\" style=\"top:${top}px;height:${h}px;left:calc(${e._l*w}% + 2px);width:calc(${w}% - 4px);background:${staffColor(e)}\"><b>${fmtTime(e.time)}</b> ${esc(e.title)}</button>`;")
new = ("      const w=100/n;\n"
       "        const isMd=!!(e._mdStart);const mdLabel=isMd&&e._mdFirst?'<b>'+fmtTime(e.time)+'</b> '+esc(e.title):isMd?'<span style=\"opacity:.6;font-size:11px\">↓ '+esc(e.title)+'</span>':'<b>'+fmtTime(e.time)+'</b> '+esc(e.title);\n"
       "        return `<button class=\"blk\" data-open=\"${esc(e.id)}\" style=\"top:${top}px;height:${h}px;left:calc(${e._l*w}% + 2px);width:calc(${w}% - 4px);background:${staffColor(e)};${isMd&&!e._mdFirst?'opacity:.75;border-top:2px solid rgba(255,255,255,.5)':''}\"><b>${isMd&&!e._mdFirst?'':fmtTime(e.time)}</b>${isMd&&!e._mdFirst?' '+esc(e.title):' '+esc(e.title)}</button>`;")

if old in html:
    html = html.replace(old, new, 1)
    print("OK: mdSpan style")
else:
    # simpler fix - just label continuation blocks differently
    idx = html.find("const w=100/n;")
    print("MISS - found w at:", idx, repr(html[idx:idx+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
