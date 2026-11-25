from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
# Find where contacts box is rendered - is it conditional on people.length?
idx = html.find("cbox_")
print(repr(html[max(0,idx-200):idx+300]))
