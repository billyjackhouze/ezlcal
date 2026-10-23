import re, sys
from pathlib import Path

f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
orig_len = len(html)

changes = 0

def rep(old, new, label):
    global html, changes
    if old in html:
        html = html.replace(old, new, 1)
        changes += 1
        print(f"OK: {label}")
    else:
        print(f"MISS: {label}")

# 1. Personal category
rep("'Travel','Company event']", "'Travel','Company event','Personal']", "Personal category")

# 2. staffColor function
rep("const catColor=c=>CATC[c]||'#5f6b7a';",
    "const catColor=c=>CATC[c]||'#5f6b7a';\nconst staffColor=e=>{if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i]){const n=STF[i][0]||'';if(/tpalmer|trey/i.test(n))return '#e53935';if(/tgreen|^tim/i.test(n))return '#2e7d32';if(/goodwin|jesse/i.test(n))return '#1565c0';if(/jvela|joey|joseph/i.test(n))return '#00796b';return '#5f6b7a';}}}return '#5f6b7a';};",
    "staffColor function")

# 3. Replace catColor(e.cat) with staffColor(e)
old_cc = "catColor(e.cat)"
count = html.count(old_cc)
html = html.replace(old_cc, "staffColor(e)")
print(f"OK: replaced {count} catColor(e.cat) calls")
changes += 1

# 4. Restore modal dot to catColor
rep('background:${staffColor(e)}"></span><h2>${esc(e.title)}</h2>',
    'background:${catColor(e.cat)}"></span><h2>${esc(e.title)}</h2>',
    "modal dot restored to catColor")

# 5. createdBy in fromServer
rep("updatedAt:e.updatedAt,updatedBy:e.updatedBy});",
    "updatedAt:e.updatedAt,updatedBy:e.updatedBy,createdBy:e.createdBy||''});",
    "createdBy in fromServer")

# 6. Permission check on edit/delete
rep("$('#m_x').onclick=closeModal;$('#m_edit').onclick=()=>openEditor(e.id);\n    $('#m_del').onclick=()=>{if(confirm('Delete \"'+e.title+'\"?')){const b=JSON.parse(JSON.stringify(e));b.deleted=true;closeModal();saveEvent(b);toast('Appointment deleted');}};",
    "$('#m_x').onclick=closeModal;\n    const _can=!e.createdBy||e.createdBy===EZ.user.username;\n    const _eb=$('#m_edit'),_db=$('#m_del');\n    if(_eb){_eb.onclick=()=>{if(_can)openEditor(e.id);else toast('Only the creator can edit this.');};_eb.style.opacity=_can?'1':'0.4';}\n    if(_db){_db.onclick=()=>{if(!_can){toast('Only the creator can delete this.');return;}if(confirm('Delete \"'+e.title+'\"?')){const b=JSON.parse(JSON.stringify(e));b.deleted=true;closeModal();saveEvent(b);toast('Appointment deleted');}};_db.style.opacity=_can?'1':'0.4';}",
    "creator-only edit/delete")

# 7. Legend - staff colors
rep('<span class="bar" style="background:#2f8f3a"></span>Customer visit / meal',
    '<span class="bar" style="background:#e53935"></span>Trey Palmer', "legend Trey")
rep('<span class="bar" style="background:#2f6fde"></span>Meeting',
    '<span class="bar" style="background:#2e7d32"></span>Tim Green', "legend Tim")
rep('<span class="bar" style="background:#d4721c"></span>Outing',
    '<span class="bar" style="background:#1565c0"></span>Jesse Goodwin', "legend Jesse")
rep('<span class="bar" style="background:#1c7c74"></span>Lunch &amp; learn / site visit',
    '<span class="bar" style="background:#00796b"></span>Joseph Vela', "legend Joey")
rep('<span class="bar" style="background:#7d4fc4"></span>Follow-up',
    '<span class="bar" style="background:#5f6b7a"></span>Other staff', "legend other")
rep('<span class="bar" style="background:#6b6b72"></span>Travel', '', "legend travel removed")

print(f"\n{changes} changes, {len(html)-orig_len:+d} bytes")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Written OK")
