from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix the broken sync line - missing semicolon after IIFE
old_broken = "d.value||'':'';})()e.cat="
new_fixed = "d.value||'':'';})();e.cat="
if old_broken in html:
    html = html.replace(old_broken, new_fixed, 1)
    print("OK: fixed missing semicolon")
else:
    print("MISS: checking sync area")
    idx = html.find("f_end_date")
    print(repr(html[max(0,idx-50):idx+100]))

# Now add the end date field cleanly after f_end input
idx2 = html.find('"f_end"')
chunk = html[idx2:idx2+80]
end_pos = idx2 + chunk.find('>') + 1
new_field = '<input type="date" id="f_end_date" value="${e.endDate||\'\'}" title="End date" aria-label="End date" style="margin-left:4px">'
html = html[:end_pos] + new_field + html[end_pos:]
print("f_end_date in html:", "f_end_date" in html)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
