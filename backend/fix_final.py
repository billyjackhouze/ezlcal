from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Replace staffColor with a version that avoids the problematic regex escape
old = re.search(r"const staffColor=e=>\{.*?return '#546e7a';\s*\};", html, re.S)
if old:
    print(f"Found staffColor at {old.start()}")
    # Simple version - match by staff name fragments, no complex regex
    new_fn = """const staffColor=e=>{
  const _sc=(n,si)=>{
    if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];
    const s=n.toLowerCase();
    if(s.indexOf('tpalmer')>=0||s.indexOf('trey')>=0)return '#c62828';
    if(s.indexOf('tgreen')>=0||s.indexOf('tim')>=0)return '#2e7d32';
    if(s.indexOf('goodwin')>=0||s.indexOf('jesse')>=0)return '#6a1b9a';
    if(s.indexOf('jvela')>=0||s.indexOf('joey')>=0||s.indexOf('joseph')>=0)return '#e65100';
    return '#546e7a';
  };
  if(e&&e.createdBy){
    const cb=e.createdBy.toLowerCase();
    const si=STF.findIndex(function(s){return s&&s[2]&&cb.indexOf(s[2].toLowerCase())>=0;});
    return _sc(e.createdBy,si);
  }
  if(e&&e.att){for(var _i=0;_i<e.att.length;_i++){var t=e.att[_i][0],i=e.att[_i][1];if(t==='s'&&i>=0&&STF[i])return _sc(STF[i][0]||'',i);}}
  return '#546e7a';
};"""
    html = html[:old.start()] + new_fn + html[old.end():]
    print("OK: staffColor replaced (no regex in JS)")
else:
    print("MISS")

# Fix _swc with indexOf too
old2 = re.search(r"const _swc=i=>\{.*?\};", html, re.S)
if old2:
    html = html[:old2.start()] + """const _swc=i=>{
  if(i<0)return '#888';
  if(STF[i]&&STF[i][3])return STF[i][3];
  var n=(STF[i]?STF[i][0]||'':'').toLowerCase();
  if(n.indexOf('tpalmer')>=0||n.indexOf('trey')>=0)return '#c62828';
  if(n.indexOf('tgreen')>=0||n.indexOf('tim')>=0)return '#2e7d32';
  if(n.indexOf('goodwin')>=0||n.indexOf('jesse')>=0)return '#6a1b9a';
  if(n.indexOf('jvela')>=0||n.indexOf('joey')>=0||n.indexOf('joseph')>=0)return '#e65100';
  return '#546e7a';
};""" + html[old2.end():]
    print("OK: _swc replaced")
else:
    print("MISS: _swc")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
