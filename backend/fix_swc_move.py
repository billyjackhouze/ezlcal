from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove _swc from its current location
old_fn = ('function _swc(i){'
    'if(i<0)return "#888";'
    'if(STF[i]&&STF[i][3])return STF[i][3];'
    'var n=(STF[i]?STF[i][0]||"":"").toLowerCase();'
    'if(n.indexOf("tpalmer")>=0||n.indexOf("trey")>=0)return "#c62828";'
    'if(n.indexOf("tgreen")>=0||n.indexOf("tim")>=0)return "#2e7d32";'
    'if(n.indexOf("goodwin")>=0||n.indexOf("jesse")>=0)return "#6a1b9a";'
    'if(n.indexOf("jvela")>=0||n.indexOf("joey")>=0||n.indexOf("joseph")>=0)return "#e65100";'
    'return "#546e7a";'
    '}')

if old_fn in html:
    html = html.replace(old_fn, '', 1)
    print("OK: removed _swc from old location")
else:
    print("MISS: _swc not found at old location")
    idx = html.find("function _swc")
    print(f"  found at {idx}: {repr(html[idx:idx+80])}")

# Insert _swc right after STF is defined inside the boot closure
anchor = "CON=D.contacts, STF=D.staff;"
new_anchor = ("CON=D.contacts, STF=D.staff;"
    "function _swc(i){"
    "if(i<0)return '#888';"
    "if(STF[i]&&STF[i][3])return STF[i][3];"
    "var n=(STF[i]?STF[i][0]||'':'').toLowerCase();"
    "if(n.indexOf('tpalmer')>=0||n.indexOf('trey')>=0)return '#c62828';"
    "if(n.indexOf('tgreen')>=0||n.indexOf('tim')>=0)return '#2e7d32';"
    "if(n.indexOf('goodwin')>=0||n.indexOf('jesse')>=0)return '#6a1b9a';"
    "if(n.indexOf('jvela')>=0||n.indexOf('joey')>=0||n.indexOf('joseph')>=0)return '#e65100';"
    "return '#546e7a';"
    "}")

if anchor in html:
    html = html.replace(anchor, new_anchor, 1)
    print("OK: _swc inserted after STF= inside boot closure")
else:
    print("MISS: anchor not found")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
