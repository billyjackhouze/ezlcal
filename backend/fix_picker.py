from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and replace renderStaffColorPicker entirely with a safe version
old = re.search(r"function renderStaffColorPicker\(el\)\{.*?^\}", html, re.S|re.M)
if not old:
    old = re.search(r"function renderStaffColorPicker\(el\)\{.*?\n\}", html, re.S)
if old:
    print(f"Found at {old.start()}, len={len(old.group())}")
    new_fn = """function renderStaffColorPicker(el){
  if(!el)return;
  var PRESETS=['#c62828','#b71c1c','#6a1b9a','#4a148c','#e65100','#f57f17','#2e7d32','#1b5e20','#0277bd','#01579b','#00695c','#004d40','#37474f','#263238'];
  var rows='';
  for(var i=0;i<STF.length;i++){
    var s=STF[i]; if(!s)continue;
    var cur=s[3]||_swc(i);
    var btns='';
    for(var p=0;p<PRESETS.length;p++){
      var c=PRESETS[p];
      btns+='<button data-si="'+i+'" data-c="'+c+'" onclick="pickStaffColor('+i+',this.dataset.c)" style="width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid '+(cur===c?'#000':'transparent')+';cursor:pointer;padding:0;flex:0 0 18px"></button>';
    }
    rows+='<tr><td style="padding:6px 8px;font-size:13px">'+esc(s[0])+'</td>'
      +'<td style="padding:6px 8px"><div style="display:flex;gap:6px;align-items:center">'
      +'<input type="color" value="'+cur+'" id="scc'+i+'" data-si="'+i+'" onchange="pickStaffColor('+i+',this.value)" style="width:36px;height:28px;border:1px solid var(--border);border-radius:4px;cursor:pointer;padding:2px">'
      +'<span id="scd'+i+'" style="display:inline-block;width:22px;height:22px;border-radius:50%;background:'+cur+'"></span>'
      +'</div></td>'
      +'<td style="padding:6px 8px"><div style="display:flex;gap:3px;flex-wrap:wrap">'+btns+'</div></td></tr>';
  }
  el.innerHTML='<table style="width:100%;border-collapse:collapse"><thead><tr>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Name</th>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Color</th>'
    +'<th style="text-align:left;font-size:12px;color:var(--sub);padding:4px 8px;font-weight:500">Presets</th>'
    +'</tr></thead><tbody>'+rows+'</tbody></table>';
}
function pickStaffColor(si,color){
  if(!STF[si])return;
  STF[si][3]=color;
  var inp=document.getElementById('scc'+si);
  var dot=document.getElementById('scd'+si);
  if(inp)inp.value=color;
  if(dot)dot.style.background=color;
  setStaffColor(STF[si][2],color);
}"""
    html = html[:old.start()] + new_fn + html[old.end():]
    print("OK: renderStaffColorPicker rewritten safely")
else:
    print("MISS: renderStaffColorPicker not found")
    idx = html.find("renderStaffColorPicker")
    print(f"  found at {idx}: {repr(html[idx:idx+100])}")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
