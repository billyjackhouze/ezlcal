from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Show full week blocks section
idx = html.find("const multiDay=evs.filter")
print(repr(html[idx:idx+500]))
