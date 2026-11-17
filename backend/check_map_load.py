from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the map API call and pin rendering
idx = html.find("/api/map")
print("API call:", repr(html[idx-20:idx+100]))
# Find where pins are filtered/rendered
idx2 = html.find("addLayer")
if idx2 < 0: idx2 = html.find("marker")
print("marker at:", idx2, repr(html[idx2:idx2+200]))
# Find Buyer filter
idx3 = html.find("Buyer")
while idx3 >= 0:
    print("Buyer ref:", repr(html[max(0,idx3-40):idx3+80]))
    idx3 = html.find("Buyer", idx3+1)
