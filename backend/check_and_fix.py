from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
idx = html.find("const timed=evs.filter(e=>e.date===ds&&e.time)")
print(repr(html[idx:idx+200]))
