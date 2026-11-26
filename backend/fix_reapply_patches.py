from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# 1. Always show contacts box - remove people.length ternary wrapper
old1 = "${people.length?`<div class=\"box\" id=\"cbox_${i}\">"
new1 = "<div class=\"box\" id=\"cbox_${i}\">"
# Find full ternary - ends with `:''}`
idx = html.find(old1)
if idx >= 0:
    # Find the closing :`''}`
    end = html.find("</div></div>`:''}",  idx)
    if end >= 0:
        close = "</div></div>`:''}"+"\n"
        old_block = html[idx:end+len("</div></div>`:''}")]
        new_block = html[idx+len("${people.length?`"):end+len("</div></div>")]
        html = html[:idx] + new_block + html[end+len("</div></div>`:''}") :]
        print("OK: contacts box always shown")
    else:
        print("MISS end")
else:
    print("MISS start")

# 2. Expose __accIds for the submit handler (K.a = account UUIDs)
old2 = "const IX={a:new Map(K.a.map((k,i)=>[k,i])),c:new Map(K.c.map((k,i)=>[k,i])),s:new Map(K.s.map((k,i)=>[k,i]))};"
new2 = old2 + "\nwindow.__accIds=K.a;"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: __accIds exposed")
else:
    print("MISS IX")

# 3. Fix submit handler to use __accIds instead of K.a
old3 = "account_id:selAcctIdx>=0?K.a[selAcctIdx]:null}"
new3 = "account_id:selAcctIdx>=0?(window.__accIds&&window.__accIds[selAcctIdx])||null:null}"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: submit uses __accIds")
else:
    print("MISS submit")

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
