from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
idx = html.find("mdEdge.map(e=>{var st=")
# Print everything from there to the end of the function
end = html.find("}).join", idx)
print(repr(html[idx:end+10]))
