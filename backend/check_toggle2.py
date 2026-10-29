from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find the contact Q boxes in template context
idx = html.find('"cqbox_${i}"')
print("cqbox in template at:", idx)
print(repr(html[idx-100:idx+200]))
print()
# Check event delegation listener
idx2 = html.find("data-toggle]')")
print("delegation listener:", repr(html[max(0,idx2-50):idx2+100]))
