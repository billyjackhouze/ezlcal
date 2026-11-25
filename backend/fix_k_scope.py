from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Add a module-level EZ._K reference when K is defined
old = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};"
new = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};EZ._K=K;EZ._IX=IX||null;"

# Actually IX is defined right after K, so just expose K via EZ after IX is defined
# Better: expose after IX line
old2 = "const IX={a:new Map(K.a.map((k,i)=>[k,i])),c:new Map(K.c.map((k,i)=>[k,i])),s:new Map(K.s.map((k,i)=>[k,i]))};"
new2 = old2 + "EZ._K=K;EZ._IX=IX;"

if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: EZ._K and EZ._IX exposed")
else:
    print("MISS on IX line")

# Fix the submit handler to use EZ._K instead of K
old3 = "account_id:selAcctIdx>=0?K.a[selAcctIdx]:null}"
new3 = "account_id:selAcctIdx>=0?(EZ._K||K).a[selAcctIdx]:null}"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: submit uses EZ._K")
else:
    print("MISS on submit handler")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
