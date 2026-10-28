from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print("toggleBox in html:", "toggleBox" in html)
print("collapsed CSS:", ".box.collapsed>.collapsible-body{display:none}" in html)
# Find toggleBox definition
idx = html.find("toggleBox")
print("First toggleBox at:", idx)
print(repr(html[idx:idx+120]))
print()
# Find the Contacts boxhead onclick
idx2 = html.find("onclick=\"toggleBox")
print("onclick toggleBox at:", idx2)
print(repr(html[idx2:idx2+60]))
