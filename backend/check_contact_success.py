from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("conAccts[newIdx]")
print(repr(html[max(0,idx-50):idx+300]))
