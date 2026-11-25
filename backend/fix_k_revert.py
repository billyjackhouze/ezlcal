from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Revert the EZ._K assignment that broke boot
old = "const IX={a:new Map(K.a.map((k,i)=>[k,i])),c:new Map(K.c.map((k,i)=>[k,i])),s:new Map(K.s.map((k,i)=>[k,i]))};EZ._K=K;EZ._IX=IX;"
new = "const IX={a:new Map(K.a.map((k,i)=>[k,i])),c:new Map(K.c.map((k,i)=>[k,i])),s:new Map(K.s.map((k,i)=>[k,i]))};"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: reverted EZ._K assignment")
else:
    print("MISS")

# Fix the submit to just use K directly - it IS in scope, the error was something else
old2 = "account_id:selAcctIdx>=0?(EZ._K||K).a[selAcctIdx]:null}"
new2 = "account_id:selAcctIdx>=0?K.a[selAcctIdx]:null}"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: reverted submit handler")
else:
    print("MISS on submit")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
