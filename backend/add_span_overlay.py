from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = "body=`<div class=\"week\" id=\"wk\">${g}</div></div>`;"
new = r"""
var _spans=evs.filter(function(e){return e.time&&e.endDate&&e.endDate>e.date;});
var _sphtml='';
if(_spans.length){
  var _N=days.length;
  _spans.forEach(function(e){
    var _d1=days.findIndex(function(d){return iso(d)===e.date;});
    var _d2=days.findIndex(function(d){return iso(d)===e.endDate;});
    if(_d1<0)return;
    var _d2c=_d2<0?_N-1:Math.min(_d2,_N-1);
    var _s=toMin(e.time),_en=e.end?toMin(e.end):_s+60;
    var _top=Math.max(0,(_s-H0*60))*48/60;
    var _h=Math.max(22,(_en-_s)*48/60);
    var _nd=_d2c-_d1+1;
    var _left='calc(56px + '+_d1+' * ((100% - 56px) / '+_N+'))';
    var _wid='calc('+_nd+' * ((100% - 56px) / '+_N+') - 4px)';
    _sphtml+='<button class="blk" data-open="'+esc(e.id)+'" style="'
      +'top:'+_top+'px;height:'+_h+'px;'
      +'left:'+_left+';width:'+_wid+';'
      +'background:'+staffColor(e)+';z-index:3;pointer-events:auto">'
      +'<b>'+fmtTime(e.time)+'</b> '+esc(e.title)+'</button>';
  });
}
body=`<div class="week" id="wk" style="position:relative">${g}${_sphtml?'<div style="position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none">'+_sphtml+'</div>':''}</div></div>`;
"""

assert old in html
html = html.replace(old, new.strip(), 1)

# Also exclude multi-day from per-column timed
old2 = "const timed=evs.filter(e=>e.date===ds&&e.time);"
new2 = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: exclude multi-day from columns")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("span-blk:", "span-blk" in html or "pointer-events:auto" in html)
print("Done", len(html))
