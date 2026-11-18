from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("function calEvents")
print(repr(html[idx:idx+300]))
idx2 = html.find("fromServer")
print("fromServer:", repr(html[idx2:idx2+200]))
