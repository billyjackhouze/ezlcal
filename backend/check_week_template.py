from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find week body assembly
idx = html.find("body=`<div class=\"week\"")
print(repr(html[idx:idx+300]))
