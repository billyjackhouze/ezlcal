from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

old = "  window.__start(D);\n  if(user.must_change)showPwChange(user);"
new = "  await Promise.resolve();\n  window.__start(D);\n  if(user.must_change)showPwChange(user);"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: deferred __start call with await Promise.resolve()")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
