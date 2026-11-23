from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find how contact sales are displayed in the account detail
idx = html.find("Sales YTD")
while idx >= 0:
    print(idx, repr(html[max(0,idx-50):idx+100]))
    idx = html.find("Sales YTD", idx+1)
    if idx > 80000: break
