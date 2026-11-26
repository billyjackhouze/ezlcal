from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove window.__S=S from where it is now (too early)
old = "window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__CON=CON;window.__STF=STF;\nwindow.__S=S;\n"
new = "window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__CON=CON;window.__STF=STF;\n"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: removed early window.__S")
else:
    print("MISS early S")

# Find where S is defined and add window.__S right after
idx = html.find("const S=")
end = html.find("\n", idx)
line = html[idx:end]
print("S defined as:", repr(line[:80]))
html = html[:end+1] + "window.__S=S;\n" + html[end+1:]
print("OK: window.__S added after S definition")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
