from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Replace K.a[selAcctIdx] with ACC[selAcctIdx][0] in the contact submit handler
# ACC is globally accessible, K is not
old = "account_id:selAcctIdx>=0?K.a[selAcctIdx]:null}"
new = "account_id:selAcctIdx>=0?ACC[selAcctIdx][0]:null}"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: replaced K.a with ACC[][0]")
else:
    print("MISS")

# Also fix K.c.push in the success handler
old2 = "const newIdx=CON.length;K.c.push(ct[0]);IX.c.set(String(ct[0]),newIdx);"
new2 = "const newIdx=CON.length;if(typeof K!=='undefined')K.c.push(ct[0]);IX.c.set(String(ct[0]),newIdx);"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: guarded K.c.push")
else:
    print("MISS on K.c.push")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
