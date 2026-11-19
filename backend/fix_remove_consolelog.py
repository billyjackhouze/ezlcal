from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and remove the console.log line
idx = html.find("console.log('mdEdge'")
if idx >= 0:
    # Find start of this statement and end
    start = html.rfind(";", 0, idx) + 1
    end = html.find(";", idx) + 1
    removed = html[start:end]
    print("Removing:", repr(removed))
    html = html[:start] + html[end:]
    print("OK: removed")
else:
    print("Not found - searching all console.log")
    idx2 = html.find("console.log")
    while idx2 >= 0:
        print(idx2, repr(html[idx2:idx2+60]))
        idx2 = html.find("console.log", idx2+1)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
