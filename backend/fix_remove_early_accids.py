from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove early window.__accIds=K.a from block 1
old = "\nwindow.__accIds=K.a;"
count = html.count(old)
print(f"Found {count} occurrences")
if count >= 1:
    html = html.replace(old, "", 1)
    print("OK: removed early __accIds")

f.write_text(html, encoding="utf-8")
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
