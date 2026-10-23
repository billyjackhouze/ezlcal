from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix staffColor colors - swap Joey and Jesse
html = html.replace("if(/goodwin|jesse/.test(cb))return '#e65100';", "if(/goodwin|jesse/.test(cb))return '#6a1b9a';")
html = html.replace("if(/jvela|joey|joseph/.test(cb))return '#6a1b9a';", "if(/jvela|joey|joseph/.test(cb))return '#e65100';")
html = html.replace("if(/goodwin|jesse/.test(n))return '#e65100';", "if(/goodwin|jesse/.test(n))return '#6a1b9a';")
html = html.replace("if(/jvela|joey|joseph/.test(n))return '#e65100';", "if(/jvela|joey|joseph/.test(n))return '#e65100';")

# Fix legend colors too
html = html.replace('background:#e65100"></span>Jesse Goodwin', 'background:#6a1b9a"></span>Jesse Goodwin')
html = html.replace('background:#6a1b9a"></span>Joseph Vela', 'background:#e65100"></span>Joseph Vela')

# Fix the syntax error in renderStaffColorPicker - replace the broken function
import re
old = re.search(r"function renderStaffColorPicker\(el\)\{.*?\}\s*(?=/\*)", html, re.S)
if old:
    print(f"Found renderStaffColorPicker, length: {len(old.group())}")
    new_fn = r"""function renderStaffColorPicker(el){
  var PRESETS=['#c62828','#b71c1c','#6a1b9a','#4a148c','#e65100','#f57f17','#2e7d32','#1b5e20','#0277bd','#01579b','#00695c','#004d40','#37474f','#263238','#4e342e','#3e2723'];
  if(!el)return;
  var rows=STF.map(function(s,i){
    if(!s)return '';
    var cur=s[3]||_swc(i);
    var presetBtns=PRESETS.map(function(c){
      return '<button onclick="STF['+i+'][3]=\''+c+'\';document.getElementById(\'scc'+i+'\').value=\''+c+'\';document.getElementById(\'scd'+i+'\').style.background=\''+c+'\';setStaffColor(\''+s[2]+'\',\''+c+'\')" style="width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid '+(cur===c?'#000':'transparent')+';cursor:pointer;padding:0;flex:0 0 18px"></button>';
    }).join('');
    return '<tr><td style="padding:6px 8px;font-size:13px">'+esc(s[0])+'</td>'
      +'<td style="padding:6px 8px"><div style="display:flex;gap:6px;align-items:center">'
      +'<input type="color" value="'+cur+'" id="scc'+i+'" onchange="STF['+i+'][3]=this.value;document.getElementById(\'scd'+i+'\').style.background=this.value;setStaffColor(\''+s[2]+'\',this.value)" style="width:36px;height:28px;border:1px solid var(--border);border-radius:4px;cursor:pointer;padding:2px">'
      +'<span id="scd'+i+'" style="display:inline-block;width:22px;height:22px;border-radius:50%;background:'+cur+'"></span>'
      +'</div></td>'
      +'<td style="padding:6px 8px"><div style="display:flex;gap:3px;flex-wrap:wrap">'+presetBtns+'</div></td></tr>';
  }).join('');
  el.innerHTML='<table style="width:100%;border-collapse:collapse"><thead><tr>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Name</th>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Color</th>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Presets</th>'
    +'</tr></thead><tbody>'+rows+'</tbody></table>';
}
"""
    html = html[:old.start()] + new_fn + html[old.end():]
    print("OK: renderStaffColorPicker rewritten safely")
else:
    print("MISS: renderStaffColorPicker not found")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
