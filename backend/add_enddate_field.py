from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find exact f_end context
idx = html.find('"f_end"')
print("Found at:", idx, repr(html[idx:idx+120]))

old = 'id="f_end" value="${e.end||\'\'}" aria-label="End time" ${e.time?\'\':\' disabled\'}><label'
alt = "id=\"f_end\" value=\"${e.end||'\\'}\" aria-label=\"End time\" ${e.time?'\\'':\\'disabled\\'}"
# Try the exact string from the output
old2 = html[idx:idx+80]
print("Trying:", repr(old2))
