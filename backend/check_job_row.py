from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("const det=[")
print(repr(html[max(0,idx-100):idx+600]))
