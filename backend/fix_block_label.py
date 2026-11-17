from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix tall block label - wrap content so title stays at top
old = "+'<b>'+fmtTime(e.time)+'</b> '+esc(e.title)+'</button>`"
# Find the actual button content in blocks render
idx = html.find("return `<button class=\"blk\"")
print(repr(html[idx:idx+300]))
