from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
old = "window.__ezl={api,fromServer,toServer,signOut,user,akey:i=>K.a[i],"
new = "window.__IX=IX;\n  window.__ezl={api,fromServer,toServer,signOut,user,akey:i=>K.a[i],"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: window.__IX exposed")
else:
    print("MISS")
old2 = "  const aIdx=IX.a.get(o.account_id);"
new2 = "  const _IX=typeof IX!=='undefined'?IX:window.__IX;\n  const aIdx=_IX&&_IX.a?_IX.a.get(o.account_id):null;"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: addPin uses window.__IX fallback")
else:
    print("MISS addPin")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
