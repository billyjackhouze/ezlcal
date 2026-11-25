from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find openNewContact function
idx = html.find("function openNewContact")
if idx < 0: idx = html.find("openNewContact")
print("openNewContact:", repr(html[idx:idx+300]))

# Find nc_x and form submit
idx2 = html.find("nc_x")
while idx2 >= 0:
    print(idx2, repr(html[max(0,idx2-30):idx2+100]))
    idx2 = html.find("nc_x", idx2+1)
    if idx2 > 100000: break
