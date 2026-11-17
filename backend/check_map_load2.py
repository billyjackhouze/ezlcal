from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the map tab rendering
idx = html.find("calMode===\\'map\\'")
if idx < 0: idx = html.find("'map'")
print("map mode at:", idx)
# Find loadMap or similar
idx2 = html.find("loadMap")
if idx2 < 0: idx2 = html.find("renderMap")
if idx2 < 0: idx2 = html.find("S.view===\\'map\\'")
print("map render at:", idx2, repr(html[idx2:idx2+200]) if idx2>=0 else "not found")
# Find fetch calls near map
idx3 = html.find("fetch(")
while idx3 >= 0:
    chunk = html[idx3:idx3+60]
    if "map" in chunk.lower() or "office" in chunk.lower():
        print("fetch:", repr(chunk))
    idx3 = html.find("fetch(", idx3+1)
