from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
# Try both encoded and unencoded versions
for old in ['<span class="bar" style="background:#1c7c74"></span>Lunch &amp; learn / site visit',
            '<span class="bar" style="background:#1c7c74"></span>Lunch & learn / site visit']:
    if old in html:
        html = html.replace(old, '<span class="bar" style="background:#00796b"></span>Joseph Vela', 1)
        print(f"Fixed: {repr(old[:60])}")
        break
else:
    # Find whatever is left with #1c7c74
    import re
    m = re.search(r'background:#1c7c74[^<]+', html)
    if m: print(f"Found: {repr(m.group())}")
    else: print("Not found at all")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
