from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the week dcol template - look for return with dcol in week section
idx = html.find("calMode==='week'")
print("week at:", idx)
# Find the dcol return in week view
idx2 = html.find("return `<div class=\"dcol", idx)
print("dcol return:", idx2, repr(html[idx2:idx2+200]))
