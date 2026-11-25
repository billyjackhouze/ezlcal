from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Expose IX globally alongside K.a
old = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};window.__accIds=K.a;"
new = "const K={a:boot.accounts.map(a=>a[0]),c:boot.contacts.map(c=>c[0]),s:boot.staff.map(s=>s[0])};window.__accIds=K.a;"
# IX is defined right after K, expose it after IX definition
old2 = "const IX={a:new Map(K.a.map((k,i)=>[k,i])),c:new Map(K.c.map((k,i)=>[k,i])),s:new Map(K.s.map((k,i)=>[k,i]))};"
new2 = old2 + "window.__IX=IX;window.__K=K;"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: IX and K exposed")
else:
    print("MISS on IX")

# Fix IX.c.set and K.c.push to use window.__IX and window.__K
old3 = "if(typeof K!=='undefined')K.c.push(ct[0]);IX.c.set(String(ct[0]),newIdx);"
new3 = "if(window.__K)window.__K.c.push(ct[0]);if(window.__IX)window.__IX.c.set(String(ct[0]),newIdx);"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: fixed K.c.push and IX.c.set")
else:
    print("MISS on K/IX usage")

# Fix IX.a.has usage in CON.push
old4 = "ct[2]!=null&&IX.a.has(ct[2])?IX.a.get(ct[2]):-1"
new4 = "ct[2]!=null&&window.__IX&&window.__IX.a.has(ct[2])?window.__IX.a.get(ct[2]):-1"
if old4 in html:
    html = html.replace(old4, new4, 1)
    print("OK: fixed IX.a.has")
else:
    print("MISS on IX.a.has")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
