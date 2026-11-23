from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find Jobs in the nav
idx = html.find(">Jobs<")
print("Jobs nav:", repr(html[max(0,idx-100):idx+50]))

# Find where the jobs page is rendered
idx2 = html.find("5,000 records")
if idx2 < 0: idx2 = html.find("records")
print("records:", repr(html[max(0,idx2-100):idx2+100]))

# Search for the jobs list render - look for the table header
idx3 = html.find("Buyer</th>")
while idx3 >= 0:
    print(idx3, repr(html[max(0,idx3-100):idx3+100]))
    idx3 = html.find("Buyer</th>", idx3+1)
    if idx3 > 100000: break
