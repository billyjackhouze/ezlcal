from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("const timed=evs.filter")
while idx >= 0:
    print(idx, repr(html[idx:idx+100]))
    idx = html.find("const timed=evs.filter", idx+1)
