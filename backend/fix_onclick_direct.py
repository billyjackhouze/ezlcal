from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Revert onclick to direct call
old = 'onclick="event.stopPropagation();window.openNewContact&&window.openNewContact(${i})"'
new = 'onclick="event.stopPropagation();openNewContact(${i})"'
count = html.count(old)
if count:
    html = html.replace(old, new)
    print(f"OK: reverted {count} onclick(s) to direct call")
else:
    print("MISS")

# Verify window.__start order
idx_call = html.find("window.__start(D)")
idx_def = html.find("window.__start=function(D)")
print(f"__start call at char: {idx_call}")
print(f"__start def at char: {idx_def}")
print(f"Definition comes {'BEFORE' if idx_def < idx_call else 'AFTER'} call - {'OK' if idx_def < idx_call else 'BROKEN'}")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
