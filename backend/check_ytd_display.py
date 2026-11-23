from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("sales YTD")
print(repr(html[max(0,idx-200):idx+400]))
