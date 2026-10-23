from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Change const _swc= to function _swc() so it gets hoisted
old = ('const _swc=function(i){'
       'if(i<0)return "#888";'
       'if(STF[i]&&STF[i][3])return STF[i][3];'
       'var n=(STF[i]?STF[i][0]||"":"").toLowerCase();'
       'if(n.indexOf("tpalmer")>=0||n.indexOf("trey")>=0)return "#c62828";'
       'if(n.indexOf("tgreen")>=0||n.indexOf("tim")>=0)return "#2e7d32";'
       'if(n.indexOf("goodwin")>=0||n.indexOf("jesse")>=0)return "#6a1b9a";'
       'if(n.indexOf("jvela")>=0||n.indexOf("joey")>=0||n.indexOf("joseph")>=0)return "#e65100";'
       'return "#546e7a";'
       '};')

new = ('function _swc(i){'
       'if(i<0)return "#888";'
       'if(STF[i]&&STF[i][3])return STF[i][3];'
       'var n=(STF[i]?STF[i][0]||"":"").toLowerCase();'
       'if(n.indexOf("tpalmer")>=0||n.indexOf("trey")>=0)return "#c62828";'
       'if(n.indexOf("tgreen")>=0||n.indexOf("tim")>=0)return "#2e7d32";'
       'if(n.indexOf("goodwin")>=0||n.indexOf("jesse")>=0)return "#6a1b9a";'
       'if(n.indexOf("jvela")>=0||n.indexOf("joey")>=0||n.indexOf("joseph")>=0)return "#e65100";'
       'return "#546e7a";'
       '}')

if old in html:
    html = html.replace(old, new, 1)
    print("OK: _swc converted to hoisted function declaration")
else:
    idx = html.find("const _swc=")
    print(f"MISS - found at {idx}: {repr(html[idx:idx+60])}")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
