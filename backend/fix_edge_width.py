from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix mdEdge blocks - make them 40% width on the right side, z-index behind regular blocks
old = ('left:1px;width:calc(100% - 2px);background:"+staffColor(e)+";opacity:.9;z-index:1\\">"')
new = ('left:1px;width:calc(60% - 2px);background:"+staffColor(e)+";opacity:.7;z-index:0\\">"')
count = html.count(old)
print(f"Found {count} occurrences")
html = html.replace(old, new)
print("OK: mdEdge narrower and behind")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
