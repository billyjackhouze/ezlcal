from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find line 630, col 287
lines = html.split("\n")
print("Line 630:", repr(lines[629][270:310]))
# Also dump area around character 287 of line 630
chars = sum(len(l)+1 for l in lines[:629])
print("Char offset:", chars+287)
print("Context:", repr(html[chars+250:chars+350]))
