from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find the accounts.map that remaps the array
idx = html.find("accounts.map(a=>[")
print(repr(html[idx:idx+300]))
