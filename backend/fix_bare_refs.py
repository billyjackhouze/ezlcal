from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Fix line 859 - remove bare CON, IX, K, conAccts, conByAcct, S references
old = "const _CON=window.__CON||CON;const _IX=window.__IX||IX;const _K=window.__K||K;const _ca=window.__conAccts||conAccts;const _cba=window.__conByAcct||conByAcct;const _S=window.__S||S;const _r=window.render||render;"
new = "const _CON=window.__CON;const _IX=window.__IX;const _K=window.__K;const _ca=window.__conAccts;const _cba=window.__conByAcct;const _S=window.__S;const _r=window.render;"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: fixed bare closure refs in success handler")
else:
    print("MISS - checking what is there")
    idx = html.find("const _CON=window.__CON")
    print(repr(html[idx:idx+200]))

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
