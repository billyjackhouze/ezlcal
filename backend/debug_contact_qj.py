from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = ("EZ.api('/contacts/'+encodeURIComponent(cid)+'/'+(t==='q'?'quotes':'jobs')).then(function(r){")
new = ("console.log('ContactQJ call',cid,t);"
       "EZ.api('/contacts/'+encodeURIComponent(cid)+'/'+(t==='q'?'quotes':'jobs')).then(function(r){"
       "console.log('ContactQJ resp',t,r&&r.status);")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: debug added")
else:
    print("MISS - searching...")
    idx = html.find("loadContactQJ")
    print(repr(html[idx:idx+300]))

f.write_text(html, encoding="utf-8")
