from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find exact boundaries of staffColor function
start = html.find("staffColor=e=>{")
end = html.find("};", start) + 2
print(f"Found staffColor from {start} to {end}")
print(f"Old: {repr(html[start:end])}")

new_fn = """staffColor=e=>{
  if(e&&e.createdBy){
    const si=STF.findIndex(s=>s&&s[2]&&new RegExp(s[2].replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'i').test(e.createdBy));
    if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];
    const cb=e.createdBy.toLowerCase();
    if(/tpalmer|trey/.test(cb))return '#c62828';
    if(/tgreen|tim/.test(cb))return '#2e7d32';
    if(/goodwin|jesse/.test(cb))return '#e65100';
    if(/jvela|joey|joseph/.test(cb))return '#6a1b9a';
    return '#546e7a';
  }
  if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i]){
    if(STF[i][3])return STF[i][3];
    const n=(STF[i][0]||'').toLowerCase();
    if(/tpalmer|trey/.test(n))return '#c62828';
    if(/tgreen|tim/.test(n))return '#2e7d32';
    if(/goodwin|jesse/.test(n))return '#e65100';
    if(/jvela|joey|joseph/.test(n))return '#6a1b9a';
    return '#546e7a';
  }}}
  return '#546e7a';
}"""

html = html[:start] + new_fn + html[end:]
print("OK: staffColor replaced")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
