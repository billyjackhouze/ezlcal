import re
from pathlib import Path

f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
print(f"Before: {len(html)} bytes")

# Fix 1: staffColor - find by braces
start = html.find("\nconst staffColor=e=>{")
if start < 0: start = html.find("const staffColor=e=>{")
depth = 0
i = start
while i < len(html):
    if html[i] == "{": depth += 1
    elif html[i] == "}":
        depth -= 1
        if depth == 0:
            end = i + 2 if html[i+1:i+2] == ";" else i + 1
            break
    i += 1
new_sc = """
const staffColor=e=>{
  var _sc=function(n,si){
    if(si>=0&&STF[si]&&STF[si][3])return STF[si][3];
    var s=n.toLowerCase();
    if(s.indexOf("tpalmer")>=0||s.indexOf("trey")>=0)return "#c62828";
    if(s.indexOf("tgreen")>=0||s.indexOf("tim")>=0)return "#2e7d32";
    if(s.indexOf("goodwin")>=0||s.indexOf("jesse")>=0)return "#6a1b9a";
    if(s.indexOf("jvela")>=0||s.indexOf("joey")>=0||s.indexOf("joseph")>=0)return "#e65100";
    return "#546e7a";
  };
  if(e&&e.createdBy){
    var cb=e.createdBy.toLowerCase();
    var si=STF.findIndex(function(sx){return sx&&sx[2]&&cb.indexOf(sx[2].toLowerCase())>=0;});
    return _sc(e.createdBy,si);
  }
  if(e&&e.att){for(var _j=0;_j<e.att.length;_j++){var t=e.att[_j][0],ix=e.att[_j][1];if(t==="s"&&ix>=0&&STF[ix])return _sc(STF[ix][0]||"",ix);}}
  return "#546e7a";
};"""
html = html[:start] + new_sc + html[end:]
print("OK: staffColor")

# Fix 2: _swc
old2 = re.search(r"const _swc=(?:i=>|function)\{?[^;]{10,200}\};", html, re.S)
if old2:
    html = html[:old2.start()] + """const _swc=function(i){
  if(i<0)return "#888";
  if(STF[i]&&STF[i][3])return STF[i][3];
  var n=(STF[i]?STF[i][0]||"":"").toLowerCase();
  if(n.indexOf("tpalmer")>=0||n.indexOf("trey")>=0)return "#c62828";
  if(n.indexOf("tgreen")>=0||n.indexOf("tim")>=0)return "#2e7d32";
  if(n.indexOf("goodwin")>=0||n.indexOf("jesse")>=0)return "#6a1b9a";
  if(n.indexOf("jvela")>=0||n.indexOf("joey")>=0||n.indexOf("joseph")>=0)return "#e65100";
  return "#546e7a";
};""" + html[old2.end():]
    print("OK: _swc")

# Fix 3: renderStaffColorPicker - find by braces
start3 = html.find("\nfunction renderStaffColorPicker")
if start3 < 0: start3 = html.find("function renderStaffColorPicker")
depth = 0
i = start3
while i < len(html):
    if html[i] == "{": depth += 1
    elif html[i] == "}":
        depth -= 1
        if depth == 0:
            end3 = i + 1
            break
    i += 1
new_picker = """
function renderStaffColorPicker(el){
  if(!el)return;
  var PRESETS=["#c62828","#b71c1c","#6a1b9a","#4a148c","#e65100","#f57f17","#2e7d32","#1b5e20","#0277bd","#01579b","#00695c","#004d40","#37474f","#263238"];
  var rows="";
  for(var i=0;i<STF.length;i++){
    var s=STF[i]; if(!s)continue;
    var cur=s[3]||_swc(i);
    var btns="";
    for(var p=0;p<PRESETS.length;p++){
      var c=PRESETS[p];
      btns+="<button data-si="+i+" data-c="+c+" onclick=\\"pickStaffColor("+i+",this.dataset.c)\\" style=\\"width:18px;height:18px;border-radius:50%;background:"+c+";border:2px solid "+( cur===c?"#000":"transparent")+";cursor:pointer;padding:0\\"></button>";
    }
    rows+="<tr><td style=\\"padding:6px 8px;font-size:13px\\">"+esc(s[0])+"</td>"
      +"<td style=\\"padding:6px 8px\\"><div style=\\"display:flex;gap:6px;align-items:center\\">"
      +"<input type=color value="+cur+" id=scc"+i+" onchange=\\"pickStaffColor("+i+",this.value)\\" style=\\"width:36px;height:28px;border:1px solid var(--border);border-radius:4px;cursor:pointer\\">"
      +"<span id=scd"+i+" style=\\"display:inline-block;width:22px;height:22px;border-radius:50%;background:"+cur+"\\"></span>"
      +"</div></td>"
      +"<td style=\\"padding:6px 8px\\"><div style=\\"display:flex;gap:3px;flex-wrap:wrap\\">"+btns+"</div></td></tr>";
  }
  el.innerHTML="<table style=\\"width:100%;border-collapse:collapse\\"><thead><tr>"
    +"<th style=\\"text-align:left;font-size:12px;color:var(--sub);padding:4px 8px\\">Name</th>"
    +"<th style=\\"text-align:left;font-size:12px;color:var(--sub);padding:4px 8px\\">Color</th>"
    +"<th style=\\"text-align:left;font-size:12px;color:var(--sub);padding:4px 8px\\">Presets</th>"
    +"</tr></thead><tbody>"+rows+"</tbody></table>";
}
function pickStaffColor(si,color){
  if(!STF[si])return;
  STF[si][3]=color;
  var inp=document.getElementById("scc"+si);
  var dot=document.getElementById("scd"+si);
  if(inp)inp.value=color;
  if(dot)dot.style.background=color;
  setStaffColor(STF[si][2],color);
}"""
html = html[:start3] + new_picker + html[end3:]
print("OK: renderStaffColorPicker")

import re
print("RegExp broken:", bool(re.search(r"new RegExp.*replace", html)))
print(f"After: {len(html)} bytes")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Written OK")
