from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("cqbox_${i}")
print(repr(html[idx-20:idx+250]))
