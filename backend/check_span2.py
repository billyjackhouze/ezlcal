from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("_d2=days.findIndex")
print(repr(html[idx-20:idx+200]))
