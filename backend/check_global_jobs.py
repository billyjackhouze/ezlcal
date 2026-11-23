from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find('id="${type}-table"')
print(repr(html[max(0,idx-200):idx+600]))
