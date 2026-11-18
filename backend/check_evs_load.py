from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find how EZ.evs gets populated
idx = html.find("EZ.evs=")
if idx < 0: idx = html.find("EZ.evs =")
print("EZ.evs assignment:", repr(html[idx:idx+100]))
# Find the loadEvents or fetch events call
idx2 = html.find("loadEvents")
if idx2 < 0: idx2 = html.find("fetchEvents")
print("load events:", idx2, repr(html[idx2:idx2+100]) if idx2>=0 else "not found")
# Find what week view calls to get events
idx3 = html.find("calMode==='week'")
print("week block:", repr(html[idx3:idx3+300]))
