from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("].filter(Boolean).join('');\n    cons")
print(repr(html[idx:idx+800]))
