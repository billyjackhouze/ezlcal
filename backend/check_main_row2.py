from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("function _renderMainQJRows")
end = html.find("\nfunction ", idx+10)
print(repr(html[idx:end]))
