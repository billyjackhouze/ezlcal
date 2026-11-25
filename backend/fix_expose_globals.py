from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Expose conByAcct and related after it's built
old = "const conByAcct={}; conAccts.forEach((set,i)=>set.forEach(a=>(conByAcct[a]=conByAcct[a]||[]).push(i)));\n"
new = old + "window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__CON=CON;window.__STF=STF;\n"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: conAccts/conByAcct/CON exposed")
else:
    print("MISS conByAcct")

# Expose render and S after they exist - find where render is assigned to window
# Already done: window.render=render; - check
if "window.render=render" in html:
    print("render already exposed")
else:
    print("render NOT exposed - check needed")

# Also expose S
if "window.__S=S" not in html:
    old2 = "window.__conAccts=conAccts;window.__conByAcct=conByAcct;window.__CON=CON;window.__STF=STF;\n"
    new2 = old2 + "window.__S=S;\n"
    if old2 in html:
        html = html.replace(old2, new2, 1)
        print("OK: S exposed")

# Fix the success handler to use window.__ versions
old3 = "conAccts[newIdx]=new Set(selAcctIdx>=0?[selAcctIdx]:[]);\n      if(selAcctIdx>=0)(conByAcct[selAcctIdx]=conByAcct[selAcctIdx]||[]).push(newIdx);\n      close();toast(\'Contact added\');\n      if(onCreated)onCreated(newIdx,ct[0]);else{S.view=\'c\';S.sel.c=newIdx;render();}"
new3 = "(window.__conAccts||conAccts)[newIdx]=new Set(selAcctIdx>=0?[selAcctIdx]:[]);\n      if(selAcctIdx>=0)((window.__conByAcct||conByAcct)[selAcctIdx]=(window.__conByAcct||conByAcct)[selAcctIdx]||[]).push(newIdx);\n      close();toast(\'Contact added\');\n      if(onCreated)onCreated(newIdx,ct[0]);else if(window.render){(window.__S||S).view=\'c\';(window.__S||S).sel.c=newIdx;window.render();}"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: success handler fixed")
else:
    print("MISS success handler")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
