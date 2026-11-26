from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# In block 2 (window.__start), after openNewContact is defined,
# immediately overwrite the block-1 stub
old = "window.openNewContact=openNewContact;window.__openNewContact=openNewContact;"
new = "window.openNewContact=openNewContact;window.__openNewContact=openNewContact;window.__start._onc=openNewContact;"
# Simpler: just find where __start body ends and add updates there
# Find the last window.X=X line in block 2
old2 = "window.wireAdmin=wireAdmin;\n})();"
new2 = "window.wireAdmin=wireAdmin;\n// refresh stubs with real functions\nwindow.openNewContact=openNewContact;\nwindow.openNewAccount=openNewAccount;\nwindow.render=render;\n})();"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: stubs refreshed at end of __start")
else:
    # Try without })();
    idx = html.find("window.wireAdmin=wireAdmin;")
    print("wireAdmin at:", idx)
    print("Context:", repr(html[idx:idx+50]))

f.write_text(html, encoding="utf-8")
$utf8nobom = New-Object System.Text.UTF8Encoding $false
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
