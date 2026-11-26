from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove the early window.__IX=IX;window.__K=K; that is in block 1 (before __start)
old = "  window.__IX=IX;window.__K=K;\n"
if old in html:
    html = html.replace(old, "", 1)
    print("OK: removed early __IX/__K assignment")
else:
    # Try to find it
    idx = html.find("window.__IX=IX")
    print("Found at:", idx)
    print("Context:", repr(html[max(0,idx-30):idx+50]))

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
