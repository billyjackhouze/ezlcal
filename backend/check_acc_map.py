from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
# Find where ACC is built from boot
idx = html.find("const ACC=")
if idx < 0: idx = html.find("ACC=boot")
if idx < 0: idx = html.find("ACC =")
print(repr(html[max(0,idx-20):idx+200]))
