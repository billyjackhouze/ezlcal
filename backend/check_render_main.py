from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("_renderMainQJRows")
while idx >= 0:
    print(idx, repr(html[idx:idx+300]))
    idx = html.find("_renderMainQJRows", idx+1)
    if idx > 100000: break
