from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find where mdEdge is defined
idx = html.find("const mdEdge=")
print("mdEdge defined at:", idx)
# Find where mdEdge.map is used in week dcol
idx2 = html.find("mdEdge.map(e=>{var st=")
print("mdEdge.map used at:", idx2)
# Find the days.map callback boundaries
idx3 = html.find("days.map(d=>{const ds=iso(d)")
print("days.map at:", idx3)
# Find closing of days.map
idx4 = html.find("}).join('')}`", idx3)
print("days.map closes at:", idx4)
print("mdEdge defined INSIDE days.map:", idx3 < idx < idx4)
print("mdEdge used INSIDE days.map:", idx3 < idx2 < idx4)
