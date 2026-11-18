from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

idx = html.find("const w=100/n;")
old = html[idx:idx+200]
print("OLD:", repr(old))

# The mdSpan blocks use left:1px;width:calc(100% - 2px) - add a right margin gap
# Find the mdSpans block render
idx2 = html.find("_mdStart:isFirst")
print("mdSpans def at:", idx2)
# Find where mdSpans blocks are rendered - look for _mdStart in the render
idx3 = html.find("e._mdStart||e.time")
print("render at:", idx3, repr(html[max(0,idx3-50):idx3+100]))
