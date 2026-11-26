from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

old = "\nrender();\n};\n</script>"
new = "\nwindow.openNewContact=openNewContact;\nwindow.openNewAccount=openNewAccount;\nwindow.render=render;\nrender();\n};\n</script>"

if old in html:
    html = html.replace(old, new, 1)
    print("OK: exposed openNewContact/openNewAccount/render at end of __start")
else:
    print("MISS")
    idx = html.find("render();\n};")
    print("Context:", repr(html[max(0,idx-30):idx+30]))

f.write_text(html, encoding="utf-8")
# Deploy
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
