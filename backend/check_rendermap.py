from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("function renderMap")
print(repr(html[idx:idx+800]))
