from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
# Expose pickStaffColor globally
old = "function pickStaffColor(si,color){"
new = "window.pickStaffColor=function pickStaffColor(si,color){"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: pickStaffColor exposed globally")
else:
    print("MISS")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
