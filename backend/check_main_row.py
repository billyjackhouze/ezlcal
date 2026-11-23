from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("function _renderMainQJRows")
print(repr(html[idx:idx+800]))
