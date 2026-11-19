from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# The day view mdEdge.map at position ~49933 needs to be removed
# Find it and replace with empty string
idx = html.find("mdEdge.map(e=>{var st=e._mdStart||e.time")
if idx < 0:
    idx = html.find("mdEdge.map(e=>{const s=toMin(e._mdStart")
print("day view mdEdge.map at:", idx)

# Find the full expression - ends with .join('')}
end = html.find(".join('')}", idx) + len(".join('')}")
print("ends at:", end)
old = html[idx:end]
print("removing:", repr(old[:80]))

html = html[:idx] + "''" + html[end:]
print("OK: day view mdEdge removed")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
