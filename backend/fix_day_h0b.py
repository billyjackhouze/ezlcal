from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find where H0 is defined vs where day view is
h0_pos = html.find("const H0=6,H1=21;")
day_pos = html.find("S.calMode==='day'")
print(f"H0 defined at: {h0_pos}")
print(f"Day view at: {day_pos}")
print(f"Day view is {'BEFORE' if day_pos < h0_pos else 'AFTER'} H0 definition")

# Fix: add H0/H1 as local vars at top of day view block
old = "  if(S.calMode==='day'){\n    const ds=iso(S.calDate);"
new = "  if(S.calMode==='day'){\n    const H0=6,H1=21;\n    const ds=iso(S.calDate);"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: H0/H1 added to day view")
    f.write_text(html, encoding="utf-8")
    Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
else:
    print("MISS - checking day view start")
    idx = html.find("calMode==='day'")
    print(repr(html[idx:idx+80]))
