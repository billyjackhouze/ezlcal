from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

old = "account_id:selAcctIdx>=0?(window.__accIds?window.__accIds[selAcctIdx]:null):null}"
new = "account_id:selAcctIdx>=0?(window.__accIds&&window.__accIds[selAcctIdx])||null:null}"
if old in html:
    html = html.replace(old, new, 1)
    print("OK")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
