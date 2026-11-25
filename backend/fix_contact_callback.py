from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# After conAccts and conByAcct are defined, expose a callback setter
# Find where conAccts is defined
idx = html.find("const conAccts=")
print("conAccts at:", idx)
end = html.find("\n", idx)
print("line:", repr(html[idx:end+1]))

# Find conByAcct
idx2 = html.find("const conByAcct=")
end2 = html.find("\n", idx2)
print("conByAcct:", repr(html[idx2:end2+1]))
