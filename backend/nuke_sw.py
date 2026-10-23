from pathlib import Path
import shutil

dist = Path(r"C:\Apps\ezlcal\backend\dist")

# Copy sw.js to sw2.js
shutil.copy(dist / "sw.js", dist / "sw2.js")
print("Copied sw.js to sw2.js")

# Update index.html to register sw2.js instead of sw.js
for p in [dist / "index.html", Path(r"C:\Apps\ezlcal\web\index.html")]:
    html = p.read_text(encoding="utf-8")
    if "sw.js" in html:
        html = html.replace("sw.js", "sw2.js")
        p.write_text(html, encoding="utf-8")
        print(f"Updated {p.name}")
