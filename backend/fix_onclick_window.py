from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

old = 'onclick="event.stopPropagation();openNewContact(${i})"'
new = 'onclick="event.stopPropagation();window.openNewContact&&window.openNewContact(${i})"'
count = html.count(old)
if count:
    html = html.replace(old, new)
    print(f"OK: fixed {count} onclick(s)")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
