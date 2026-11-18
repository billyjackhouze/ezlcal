from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Check how H0/H1 are defined
idx = html.find("const H0=")
if idx < 0: idx = html.find("H0=")
print("H0 def:", repr(html[idx:idx+60]))

# Check if H0 is exposed as window.__H0
idx2 = html.find("window.__H0")
print("window.__H0:", idx2)
