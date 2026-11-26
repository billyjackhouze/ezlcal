from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Add a global stub right after the toggleQJDetail assignment in block 1
old = "window.toggleQJDetail=toggleQJDetail;\nwindow.filterQJTable=filterQJTable;\nwindow.filterMainQJTable=f"
new = "window.toggleQJDetail=toggleQJDetail;\nwindow.filterQJTable=filterQJTable;\nwindow.filterMainQJTable=f"
# Just add the stub after the existing window assignments block
# Find end of the window assignments section in block 1
old2 = "window.toggleQJDetail=toggleQJDetail;\nwindow.filterQJTable=filterQJTable;\nwindow.filterMainQJTable=filterMainQJTable;\n"
if old2 in html:
    new2 = old2 + "window.openNewContact=function(){if(window.__openNewContact)window.__openNewContact.apply(this,arguments);};\nwindow.openNewAccount=function(){if(window.__openNewAccount)window.__openNewAccount.apply(this,arguments);};\n"
    html = html.replace(old2, new2, 1)
    print("OK: stubs added in block 1")
else:
    print("MISS - checking what follows filterMainQJTable")
    idx = html.find("window.filterMainQJTable=filterMainQJTable")
    print(repr(html[idx:idx+100]))

# In block 2 where real functions are defined, assign to __openNewContact
old3 = "window.openNewContact=openNewContact;"
new3 = "window.openNewContact=openNewContact;window.__openNewContact=openNewContact;"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: __openNewContact set in block 2")

old4 = "window.openNewAccount=openNewAccount;"
new4 = "window.openNewAccount=openNewAccount;window.__openNewAccount=openNewAccount;"
if old4 in html:
    html = html.replace(old4, new4, 1)
    print("OK: __openNewAccount set in block 2")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
