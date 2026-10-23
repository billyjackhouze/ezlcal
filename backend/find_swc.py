import re
from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
calls = [(m.start(), html[max(0,m.start()-30):m.start()+60]) for m in re.finditer(r"_swc\(", html)]
for pos, ctx in calls:
    print(f"Call at {pos}: {repr(ctx)}")
defn = html.find("const _swc=")
print(f"_swc defined at: {defn}")
