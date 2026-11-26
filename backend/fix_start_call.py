from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove __start call from block 1, save the surrounding context
old1 = "  window.__start(D);\n  if(user.must_change)showPwChange(user);\n}"
new1 = "  window.__pendingBoot={D,user};\n  if(window.__start)window.__start(D);\n  if(user.must_change)showPwChange(user);\n}"
if old1 in html:
    html = html.replace(old1, new1, 1)
    print("OK: block 1 saves boot data, calls __start if available")
else:
    print("MISS block 1")

# At start of block 2 __start definition, check for pending boot
old2 = "window.__start=function(D){\n'use strict';"
new2 = "window.__start=function(D){\n'use strict';"
# At end of block 2, after all defs, pick up pending boot if any
old3 = "window.wireAdmin=wireAdmin;\n})();"
new3 = "window.wireAdmin=wireAdmin;\nif(window.__pendingBoot&&!window.__startRan){window.__startRan=true;const _pb=window.__pendingBoot;window.__start(_pb.D);if(_pb.user&&_pb.user.must_change)showPwChange(_pb.user);}\n})();"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print("OK: block 2 picks up pending boot")
else:
    idx = html.find("window.wireAdmin=wireAdmin;")
    print("MISS block 2 end, wireAdmin at:", idx)
    print(repr(html[idx:idx+60]))

f.write_text(html, encoding="utf-8")
# Deploy
utf8nobom = "utf-8"
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
