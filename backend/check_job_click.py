from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find job row click handler
idx = html.find("data-job")
while idx >= 0:
    print(idx, repr(html[max(0,idx-30):idx+100]))
    idx = html.find("data-job", idx+1)
    if idx > 80000: break
