from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Add more globals at end of __start, before render()
old = "\nwindow.openNewContact=openNewContact;\nwindow.openNewAccount=openNewAccount;\nwindow.render=render;\nrender();\n};\n</script>"
new = "\nwindow.openNewContact=openNewContact;\nwindow.openNewAccount=openNewAccount;\nwindow.render=render;\nwindow.__IX=IX;window.__K=K;window.__CON=CON;window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__S=S;\nrender();\n};\n</script>"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: all globals exposed")
else:
    print("MISS")

# Fix success handler to use window.__ versions for all closure vars
old2 = "const ct=j.contact;const newIdx=CON.length;K.c.push(ct[0]);IX.c.set(String(ct[0]),newIdx);\n      CON.push([ct[1],ct[2]!=null&&IX.a.has(ct[2])?IX.a.get(ct[2]):-1,ct[3]||'',ct[4]||'',ct[5]||'',ct[6]||'','','','','','',false,true]);\n      conAccts[newIdx]=new Set(selAcctIdx>=0?[selAcctIdx]:[]);\n      if(selAcctIdx>=0)(conByAcct[selAcctIdx]=conByAcct[selAcctIdx]||[]).push(newIdx);\n      close();toast('Contact added');\n      if(onCreated)onCreated(newIdx,ct[0]);else{S.view='c';S.sel.c=newIdx;render();}"
new2 = "const ct=j.contact;const _CON=window.__CON||CON;const _IX=window.__IX||IX;const _K=window.__K||K;const _ca=window.__conAccts||conAccts;const _cba=window.__conByAcct||conByAcct;const _S=window.__S||S;const _r=window.render||render;const newIdx=_CON.length;_K.c.push(ct[0]);_IX.c.set(String(ct[0]),newIdx);\n      _CON.push([ct[1],ct[2]!=null&&_IX.a.has(ct[2])?_IX.a.get(ct[2]):-1,ct[3]||'',ct[4]||'',ct[5]||'',ct[6]||'','','','','','',false,true]);\n      _ca[newIdx]=new Set(selAcctIdx>=0?[selAcctIdx]:[]);\n      if(selAcctIdx>=0)(_cba[selAcctIdx]=_cba[selAcctIdx]||[]).push(newIdx);\n      close();toast('Contact added');\n      if(onCreated)onCreated(newIdx,ct[0]);else{_S.view='c';_S.sel.c=newIdx;_r();}"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: success handler fixed")
else:
    print("MISS success handler")

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
