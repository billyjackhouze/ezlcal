from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find Add contact button render
idx = html.find("Add contact")
while idx >= 0:
    print(idx, repr(html[max(0,idx-80):idx+120]))
    idx = html.find("Add contact", idx+1)
    if idx > 80000: break
