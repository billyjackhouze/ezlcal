from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# After K is defined, expose K.a as window.__accIds
old = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};"
new = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};window.__accIds=K.a;"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: window.__accIds exposed")
else:
    print("MISS")

# Fix submit to use window.__accIds
old2 = "account_id:selAcctIdx>=0?ACC[selAcctIdx][0]:null}"
new2 = "account_id:selAcctIdx>=0?(window.__accIds?window.__accIds[selAcctIdx]:null):null}"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: submit uses __accIds")
else:
    print("MISS on submit")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
