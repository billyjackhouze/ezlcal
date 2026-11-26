from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove window.__start(D) call from block 1
old1 = "  window.__start(D);\n  if(user.must_change)showPwChange(user);\n}"
new1 = "  window.__start(D,user);\n  if(user.must_change)showPwChange(user);\n}"
# Check if __start already takes user param
print("Current call:", repr(html[html.find("window.__start(D)"):html.find("window.__start(D)")+40]))

# Check __start signature
print("__start sig:", repr(html[html.find("window.__start=function(D)"):html.find("window.__start=function(D)")+30]))
