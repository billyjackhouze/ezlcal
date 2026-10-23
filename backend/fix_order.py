from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix _swc to be self-contained - no dependency on _staffColorByName
import re
old = re.search(r"const _swc=i=>\{[^;]+\};", html)
if old:
    print(f"Found _swc: {repr(old.group()[:80])}")
    html = html[:old.start()] + """const _swc=i=>{
  if(i<0)return '#888';
  if(STF[i]&&STF[i][3])return STF[i][3];
  const n=(STF[i]?STF[i][0]||'':'').toLowerCase();
  if(/tpalmer|trey/.test(n))return '#c62828';
  if(/tgreen|tim/.test(n))return '#2e7d32';
  if(/goodwin|jesse/.test(n))return '#6a1b9a';
  if(/jvela|joey|joseph/.test(n))return '#e65100';
  return '#546e7a';
};""" + html[old.end():]
    print("OK: _swc self-contained")
else:
    print("MISS: _swc not found")

# Fix staffColor to also be self-contained (remove _staffColorByName dependency)
old2 = re.search(r"const DEFAULT_STAFF_COLORS=.*?const staffColor=.*?\};", html, re.S)
if old2:
    print(f"Found DEFAULT_STAFF_COLORS block")
    html = html[:old2.start()] + """const staffColor=e=>{
  const _sc=(n,si)=>{
    if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];
    const s=n.toLowerCase();
    if(/tpalmer|trey/.test(s))return '#c62828';
    if(/tgreen|tim/.test(s))return '#2e7d32';
    if(/goodwin|jesse/.test(s))return '#6a1b9a';
    if(/jvela|joey|joseph/.test(s))return '#e65100';
    return '#546e7a';
  };
  if(e&&e.createdBy){
    const si=STF.findIndex(s=>s&&s[2]&&new RegExp(s[2].replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'i').test(e.createdBy));
    return _sc(e.createdBy,si);
  }
  if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i])return _sc(STF[i][0]||'',i);}}
  return '#546e7a';
};""" + html[old2.end():]
    print("OK: staffColor self-contained")
else:
    # Try just finding old staffColor
    old3 = re.search(r"const staffColor=e=>\{.*?\};", html, re.S)
    if old3:
        print(f"Found staffColor: {repr(old3.group()[:80])}")
        html = html[:old3.start()] + """const staffColor=e=>{
  const _sc=(n,si)=>{
    if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];
    const s=n.toLowerCase();
    if(/tpalmer|trey/.test(s))return '#c62828';
    if(/tgreen|tim/.test(s))return '#2e7d32';
    if(/goodwin|jesse/.test(s))return '#6a1b9a';
    if(/jvela|joey|joseph/.test(s))return '#e65100';
    return '#546e7a';
  };
  if(e&&e.createdBy){
    const si=STF.findIndex(s=>s&&s[2]&&new RegExp(s[2].replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'i').test(e.createdBy));
    return _sc(e.createdBy,si);
  }
  if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i])return _sc(STF[i][0]||'',i);}}
  return '#546e7a';
};""" + html[old3.end():]
        print("OK: staffColor replaced")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
