from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

idx = html.find("mdEdge.map(e=>{var st=")
print(repr(html[idx:idx+600]))

# Fix: replace the label part
old = (";opacity:.85;z-index:1\"><b>'+(e._isEdge&&e.endDate===ds?'→ ends '"
       "+fmtTime(e._mdEnd):fmtTime(e.time))+'</b> '+esc(e.title)+'</button>';")
new = (";opacity:.85;z-index:1\"><b>'+(e.endDate===ds?'→ '+fmtTime(e._mdEnd):fmtTime(st))+'</b> '+esc(e.title)+'</button>';")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: label fixed")
else:
    # find the exact label
    idx2 = html.find("opacity:.85;z-index:1")
    print("label area:", repr(html[idx2:idx2+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
