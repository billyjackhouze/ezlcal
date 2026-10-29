from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find how K.c is built
idx = html.find("K={a:")
print(repr(html[idx:idx+300]))
