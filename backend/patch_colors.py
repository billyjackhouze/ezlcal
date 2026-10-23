from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
orig = len(html)

def rep(old, new, label):
    global html
    if old in html:
        html = html.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"MISS: {label}")

# 1. Remove creator restriction
rep("""$('#m_x').onclick=closeModal;
    const _can=!e.createdBy||e.createdBy===EZ.user.username;
    const _eb=$('#m_edit'),_db=$('#m_del');
    if(_eb){_eb.onclick=()=>{if(_can)openEditor(e.id);else toast('Only the creator can edit this.');};_eb.style.opacity=_can?'1':'0.4';}
    if(_db){_db.onclick=()=>{if(!_can){toast('Only the creator can delete this.');return;}if(confirm('Delete "'+e.title+'"?')){const b=JSON.parse(JSON.stringify(e));b.deleted=true;closeModal();saveEvent(b);toast('Appointment deleted');}};_db.style.opacity=_can?'1':'0.4';}""",
    """$('#m_x').onclick=closeModal;$('#m_edit').onclick=()=>openEditor(e.id);\n    $('#m_del').onclick=()=>{if(confirm('Delete "'+e.title+'"?')){const b=JSON.parse(JSON.stringify(e));b.deleted=true;closeModal();saveEvent(b);toast('Appointment deleted');}};""",
    "removed creator restriction")

# 2. STF remap to include id and cal_color
rep("staff:boot.staff.map(s=>[s[1],s[2]||'']),",
    "staff:boot.staff.map(s=>[s[1],s[2]||'',s[0]||'',s[3]||'']),",
    "STF includes id and cal_color")

# 3. New staffColor with DB color support
old_fn = """function _staffColorByName(n){
  if(/tpalmer|trey/i.test(n))return '#c62828';
  if(/tgreen|^tim/i.test(n))return '#2e7d32';
  if(/goodwin|jesse/i.test(n))return '#e65100';
  if(/jvela|joey|joseph/i.test(n))return '#00695c';
  if(/bsimpson|billy/i.test(n))return '#6a1020';
  return '#546e7a';
}
const staffColor=e=>{
  // Color by creator first, fall back to first staff attendee
  if(e&&e.createdBy){const cb=e.createdBy;return _staffColorByName(cb);}
  if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i]){return _staffColorByName(STF[i][0]||'');}}}
  return '#546e7a';
};"""
new_fn = """const DEFAULT_STAFF_COLORS={'tpalmer':'#c62828','trey':'#c62828','tgreen':'#2e7d32','tim':'#2e7d32','goodwin':'#e65100','jesse':'#e65100','jvela':'#6a1b9a','joey':'#6a1b9a','joseph':'#6a1b9a','bsimpson':'#37474f','billy':'#37474f'};
function _staffColorByName(n,si){if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];const k=Object.keys(DEFAULT_STAFF_COLORS).find(k=>new RegExp(k,'i').test(n));return k?DEFAULT_STAFF_COLORS[k]:'#546e7a';}
function _staffIdxByUsername(cb){if(!cb)return -1;return STF.findIndex(s=>s&&s[2]&&new RegExp(s[2].replace(/[.*+?^${}()|[\]\\\\]/g,'\\\\$&'),'i').test(cb));}
const staffColor=e=>{if(e&&e.createdBy){const si=_staffIdxByUsername(e.createdBy);return _staffColorByName(e.createdBy,si);}if(e&&e.att){for(const [t,i] of e.att){if(t==='s'&&i>=0&&STF[i]){return _staffColorByName(STF[i][0]||'',i);}}}return '#546e7a';};"""
rep(old_fn, new_fn, "staffColor with DB color")

# 4. Update _swc
rep("const _swc=i=>{if(i<0)return '#888';if(STF[i]&&STF[i][3])return STF[i][3];return _staffColorByName(STF[i]?STF[i][0]||'':'',i);};",
    "const _swc=i=>{if(i<0)return '#888';if(STF[i]&&STF[i][3])return STF[i][3];return _staffColorByName(STF[i]?STF[i][0]||'':'',i);};",
    "_swc already correct (no change)")

# 5. Joey legend purple
rep("background:#00695c\"></span>Joseph Vela",
    "background:#6a1b9a\"></span>Joseph Vela", "Joey legend purple")

# 6. Add staff color picker function before admin section
old_admin = "/* ---------- admin ---------- */"
new_fn_block = """/* ---------- staff color picker ---------- */
async function setStaffColor(staffId,color){
  const r=await EZ.api('/staff/'+encodeURIComponent(staffId)+'/color',{method:'PUT',body:JSON.stringify({color})});
  if(r&&r.ok)toast('Color saved');else toast('Failed to save');
}
function renderStaffColorPicker(el){
  const PRESETS=['#c62828','#b71c1c','#e65100','#f57f17','#2e7d32','#1b5e20','#6a1b9a','#4a148c','#0277bd','#01579b','#00695c','#004d40','#37474f','#263238','#4e342e','#3e2723'];
  if(!el)return;
  el.innerHTML='<table style="width:100%;border-collapse:collapse">'+
    '<thead><tr><th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Name</th><th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Color</th><th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Presets</th></tr></thead><tbody>'+
    STF.map((s,i)=>{if(!s)return '';const cur=s[3]||_swc(i);return '<tr><td style="padding:6px 8px;font-size:13px">'+esc(s[0])+'</td>'+
      '<td style="padding:6px 8px"><div style="display:flex;gap:6px;align-items:center">'+
      '<input type="color" value="'+cur+'" id="scc_'+i+'" onchange="STF['+i+'][3]=this.value;document.getElementById(\'scd_'+i+'\').style.background=this.value;setStaffColor('+JSON.stringify(s[2])+',this.value)" style="width:36px;height:28px;border:1px solid var(--border);border-radius:4px;cursor:pointer;padding:2px">'+
      '<span id="scd_'+i+'" style="display:inline-block;width:22px;height:22px;border-radius:50%;background:'+cur+'"></span></div></td>'+
      '<td style="padding:6px 8px"><div style="display:flex;gap:3px;flex-wrap:wrap">'+PRESETS.map(c=>'<button onclick="STF['+i+'][3]=\''+c+'\';document.getElementById(\'scc_'+i+'\').value=\''+c+'\';document.getElementById(\'scd_'+i+'\').style.background=\''+c+'\';setStaffColor('+JSON.stringify(s[2])+',\''+c+'\')" style="width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid '+(cur===c?'#000':'transparent')+';cursor:pointer;padding:0"></button>').join('')+'</div></td></tr>';}).join('')+
    '</tbody></table>';
}
/* ---------- admin ---------- */"""
rep(old_admin, new_fn_block, "color picker function")

# 7. Add color picker to admin panel
rep("in the invitee list.</p></div>`;\n  wireAdmin(main)",
    "in the invitee list.</p></div>\n  <div class=\"box\" style=\"margin-top:16px\"><div class=\"boxhead\"><b>Staff Calendar Colors</b></div><div id=\"staff-color-picker\" style=\"padding:10px 14px\"></div></div>`;\n  wireAdmin(main);\n  requestAnimationFrame(()=>{const el=document.getElementById('staff-color-picker');if(el)renderStaffColorPicker(el);})",
    "color picker in admin panel")

print(f"\n{len(html)-orig:+d} bytes")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Written OK")
