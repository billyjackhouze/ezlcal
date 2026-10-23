from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
idx = html.find("const _swc=")
end = html.index(";", idx+50)+1
print("Found:", repr(html[idx:end][:100]))
new_swc = (
    'const _swc=function(i){'
    'if(i<0)return "#888";'
    'if(STF[i]&&STF[i][3])return STF[i][3];'
    'var n=(STF[i]?STF[i][0]||"":"").toLowerCase();'
    'if(n.indexOf("tpalmer")>=0||n.indexOf("trey")>=0)return "#c62828";'
    'if(n.indexOf("tgreen")>=0||n.indexOf("tim")>=0)return "#2e7d32";'
    'if(n.indexOf("goodwin")>=0||n.indexOf("jesse")>=0)return "#6a1b9a";'
    'if(n.indexOf("jvela")>=0||n.indexOf("joey")>=0||n.indexOf("joseph")>=0)return "#e65100";'
    'return "#546e7a";'
    '};'
)
html = html[:idx] + new_swc + html[end:]
print("staffColorByName remaining:", "staffColorByName" in html)
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
