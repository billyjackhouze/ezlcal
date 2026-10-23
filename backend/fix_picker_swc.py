from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Add a standalone _getStaffColor at the top of renderStaffColorPicker
# that doesnt depend on _swc
old = "function renderStaffColorPicker(el){"
new = ("function _getStaffColor(s){"
    "if(s&&s[3])return s[3];"
    "var n=(s?s[0]||'':'').toLowerCase();"
    "if(n.indexOf('tpalmer')>=0||n.indexOf('trey')>=0)return '#c62828';"
    "if(n.indexOf('tgreen')>=0||n.indexOf('tim')>=0)return '#2e7d32';"
    "if(n.indexOf('goodwin')>=0||n.indexOf('jesse')>=0)return '#6a1b9a';"
    "if(n.indexOf('jvela')>=0||n.indexOf('joey')>=0||n.indexOf('joseph')>=0)return '#e65100';"
    "return '#546e7a';}"
    "function renderStaffColorPicker(el){")

# Also replace _swc(i) calls inside renderStaffColorPicker with _getStaffColor(STF[i])
if old in html:
    html = html.replace(old, new, 1)
    print("OK: added _getStaffColor")
    # Replace _swc(i) inside the picker function
    import re
    # Find the picker function and replace _swc(i) with _getStaffColor(s) where s is already in scope
    html = html.replace("var cur=s[3]||_swc(i);", "var cur=_getStaffColor(s);", 1)
    print("OK: replaced _swc(i) in picker")
else:
    print("MISS: renderStaffColorPicker not found")

print("_swc in renderStaffColorPicker remaining:", "renderStaffColorPicker" in html and "_swc" in html[html.find("renderStaffColorPicker"):html.find("renderStaffColorPicker")+500])

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
