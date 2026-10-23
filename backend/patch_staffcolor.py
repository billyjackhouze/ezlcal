from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and replace the old staffColor function
import re
old = re.search(r"const staffColor=e=>\{if\(e&&e\.att\).*?\}return '#546e7a';\};", html, re.S)
if old:
    print(f"Found old staffColor at {old.start()}: {repr(old.group()[:80])}")
    new_fn = """const DEFAULT_STAFF_COLORS={'tpalmer':'#c62828','trey':'#c62828','tgreen':'#2e7d32','tim':'#2e7d32','goodwin':'#e65100','jesse':'#e65100','jvela':'#6a1b9a','joey':'#6a1b9a','joseph':'#6a1b9a','bsimpson':'#37474f','billy':'#37474f'};
function _staffColorByName(n,si){if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];const k=Object.keys(DEFAULT_STAFF_COLORS).find(k=>new RegExp(k,'i').test(n));return k?DEFAULT_STAFF_COLORS[k]:'#546e7a';}
const staffColor=e=>{if(e&&e.createdBy){const si=STF.findIndex(s=>s&&s[2]&&new RegExp(s[2],'i').test(e.createdBy));return _staffColorByName(e.createdBy,si);}if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i]){return _staffColorByName(STF[i][0]||'',i);}}}return '#546e7a';};"""
    html = html[:old.start()] + new_fn + html[old.end():]
    print("OK: staffColor replaced")
else:
    print("MISS: staffColor not found by regex")
    # Show what is there
    idx = html.find("staffColor=e=>")
    print(f"  staffColor at {idx}: {repr(html[idx:idx+200])}")

# Also fix _swc to use DB color
old_swc = re.search(r"const _swc=i=>\{[^}]+\};", html)
if old_swc:
    print(f"Found _swc: {repr(old_swc.group()[:80])}")
    html = html[:old_swc.start()] + "const _swc=i=>{if(i<0)return '#888';if(STF[i]&&STF[i][3])return STF[i][3];return _staffColorByName(STF[i]?STF[i][0]||'':'',i);};" + html[old_swc.end():]
    print("OK: _swc updated")

# Fix Joey legend
html = html.replace('background:#00695c"></span>Joseph Vela', 'background:#6a1b9a"></span>Joseph Vela')
print("OK: Joey legend purple")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
