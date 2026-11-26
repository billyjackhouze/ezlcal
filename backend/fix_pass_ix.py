from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Pass IX and K through D object so __start can access them
old1 = "  await Promise.resolve();\n  window.__start(D);"
new1 = "  await Promise.resolve();\n  D.__IX=IX;D.__K=K;\n  window.__start(D);"
if old1 in html:
    html = html.replace(old1, new1, 1)
    print("OK: IX and K passed through D")
else:
    print("MISS - trying without await")
    old1b = "  window.__start(D);"
    if old1b in html:
        html = html.replace(old1b, "  D.__IX=IX;D.__K=K;\n  window.__start(D);", 1)
        print("OK: IX and K passed through D (no await)")

# In __start, use D.__IX and D.__K instead
old2 = "window.__IX=IX;window.__K=K;window.__CON=CON;window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__S=S;"
new2 = "window.__IX=D.__IX;window.__K=D.__K;window.__CON=CON;window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__S=S;window.__accIds=D.__K?D.__K.a:null;"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: __start uses D.__IX and D.__K")
else:
    print("MISS old2")

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
