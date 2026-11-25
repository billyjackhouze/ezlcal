from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
# Find D definition and ACC assignment
idx = html.find("const ACC=D.accounts")
print(repr(html[max(0,idx-50):idx+200]))
# Find where ACC[i][0] is used as a name display
idx2 = html.find("ACC[i][0]")
if idx2 < 0: idx2 = html.find("ACC[n][0]")
print("\nACC[n][0] usage:", repr(html[max(0,idx2-50):idx2+100]))
# Check what index is the name
idx3 = html.find("esc(ACC[")
print("\nesc(ACC[:", repr(html[idx3:idx3+60]))
