from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Fix chevron size
old = ".collapse-chevron{margin-left:auto;font-size:11px;transition:transform .2s;color:var(--sub)}"
new = ".collapse-chevron{margin-left:auto;font-size:22px;line-height:1;transition:transform .2s;color:var(--sub);padding:0 4px}"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: chevron size")
else:
    print("chevron already updated or missing")

# 2. Add toggleBox if missing
if "toggleBox" not in html:
    old_fn = "window.toggleCalWho="
    new_fn = "window.toggleBox=function(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');};window.toggleCalWho="
    assert old_fn in html
    html = html.replace(old_fn, new_fn, 1)
    print("OK: toggleBox added")
else:
    print("toggleBox already present")

# 3. Verify collapsed CSS is there
print("collapsed CSS:", ".box.collapsed" in html)
print("collapsible-body CSS:", ".box.collapsed>.collapsible-body{display:none}" in html)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
