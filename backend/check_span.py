from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print("span-blk:", "span-blk" in html)
print("_spans=evs", "_spans=evs" in html)
print("span-overlay:", "span-overlay" in html)
idx = html.find("body=`<div")
print("body assembly:", repr(html[idx:idx+100]))
