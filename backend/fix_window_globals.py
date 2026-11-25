import re
from pathlib import Path

f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Find all functions called from onclick/oninput attributes
onclick_fns = set(re.findall(r'onclick="([a-zA-Z_][a-zA-Z0-9_]*)\(', html))
oninput_fns = set(re.findall(r'oninput="([a-zA-Z_][a-zA-Z0-9_]*)\(', html))
attr_fns = onclick_fns | oninput_fns
print("Functions called from attributes:", sorted(attr_fns))

# Find which are defined inside the closure and not yet on window
closure_start = html.find("(function(")
closure_end = html.rfind("})()")
missing = []
for fn in sorted(attr_fns):
    idx = html.find(f"function {fn}")
    if idx < 0 or idx > closure_end:
        continue
    if idx > closure_start and f"window.{fn}" not in html:
        missing.append(fn)

print("Need window assignment:", missing)

# Add window assignments before the closing of the closure
assignments = "\n".join(f"window.{fn}={fn};" for fn in missing)
# Insert before the last })() 
old = "})();"
# Find the last one
last_idx = html.rfind(old)
new_html = html[:last_idx] + assignments + "\n" + html[last_idx:]
print("Inserting before position:", last_idx)

f.write_text(new_html, encoding="utf-8")

# Deploy
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Done")
