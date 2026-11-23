from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find kids index build
idx = html.find("kids=")
if idx < 0: idx = html.find("const kids")
print("kids:", repr(html[idx:idx+200]))

# Find famTot
idx2 = html.find("famTot=fam.reduce")
print("\nfamTot:", repr(html[idx2:idx2+150]))

# Find family function
idx3 = html.find("function family(")
print("\nfamily():", repr(html[idx3:idx3+300]))
