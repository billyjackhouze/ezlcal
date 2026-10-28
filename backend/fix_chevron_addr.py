from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Bigger chevron
old = ".collapse-chevron{margin-left:auto;font-size:11px;transition:transform .2s;color:var(--sub)}"
new = ".collapse-chevron{margin-left:auto;font-size:22px;line-height:1;transition:transform .2s;color:var(--sub);padding:0 4px}"
assert old in html
html = html.replace(old, new, 1)
print("OK: chevron size")

# 2. Company addresses - the Offices section filters by office_type
# Check what officeCard renders and what offs contains
# offs comes from offices filtered by account - need to see the filter
idx = html.find("const offs=")
print(f"offs at {idx}:", repr(html[idx:idx+120]))
