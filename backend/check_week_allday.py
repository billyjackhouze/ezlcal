from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Get full context around the week allday row at 50578
print(repr(html[50450:50750]))
