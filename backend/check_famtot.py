from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find famTot definition
idx = html.find("famTot")
while idx >= 0:
    print(idx, repr(html[max(0,idx-50):idx+120]))
    idx = html.find("famTot", idx+1)
    if idx > 100000: break

# Find account array index mapping
idx2 = html.find("ACC=D.accounts")
print("\nACC parsing:", repr(html[idx2:idx2+300]))
