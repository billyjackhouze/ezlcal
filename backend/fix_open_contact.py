from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Find all function names after stopPropagation in onclick attrs
import re
all_fns = set(re.findall(r'[;"]([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', html))

closure_start = html.find("(function(")
closure_end = html.rfind("})()")

missing = []
for fn in sorted(all_fns):
    idx = html.find(f"function {fn}")
    if idx < 0 or idx > closure_end:
        continue
    if idx > closure_start and f"window.{fn}" not in html:
        missing.append(fn)

print("Missing window assignments:", missing)

# Add them before the closure closing
if missing:
    assignments = "\n".join(f"window.{fn}={fn};" for fn in missing)
    last_idx = html.rfind("})()")
    html = html[:last_idx] + assignments + "\n" + html[last_idx:]
    f.write_text(html, encoding="utf-8")
    # Deploy
    open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
    print("Fixed and deployed")
