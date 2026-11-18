from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# 1. Update categories
old_catc = "const CATC={'Luncheon':'#2f8f3a','Breakfast':'#2f8f3a','Dinner':'#2f8f3a','Lunch and learn':'#1c7c74','Outing':'#d4721c','Meeting':'#2f6fde','Site visit':'#1c7c74','Travel':'#6b6b72','Follow-up':'#7d4fc4','Trade show':'#b5487a','Company event':'#a8862a','Appointment':'#2f6fde'};"
new_catc = "const CATC={'Sales':'#2f6fde','Lunch':'#2f8f3a','Dinner':'#1c7c74','Trade show':'#b5487a','Personal':'#6b6b72'};"
if old_catc in html:
    html = html.replace(old_catc, new_catc, 1)
    print("OK: CATC")

old_cats = "const CATS=['Luncheon','Breakfast','Dinner','Lunch and learn','Meeting','Site visit','Outing','Trade show','Follow-up','Travel','Company event','Personal'];"
new_cats = "const CATS=['Sales','Lunch','Dinner','Trade show','Personal'];"
if old_cats in html:
    html = html.replace(old_cats, new_cats, 1)
    print("OK: CATS")

# 2. Add Day view button
old_view = "[['week','Week'],['month','Month'],['list','List']].map(([k,l])=>`<button data-calmode=\"${k}\" aria-pressed=\"${S.calMode===k}\">${l}</button>`).join('')"
new_view = "[['day','Day'],['week','Week'],['month','Month'],['list','List']].map(([k,l])=>`<button data-calmode=\"${k}\" aria-pressed=\"${S.calMode===k}\">${l}</button>`).join('')"
if old_view in html:
    html = html.replace(old_view, new_view, 1)
    print("OK: Day button")

# 3. Month view - show all events
old_month = "es.slice(0,3).map(e=>`<button class=\"adb\" data-open=\"${esc(e.id)}\" style=\"background:${staffColor(e)}\">${e.time?fmtTime(e.time).replace(':00','')+' ':''}${esc(e.title)}</button>`).join('')}${es.length>3?`<button class=\"more\" data-calmode=\"list\">+${es.length-3} more</button>`:''}"
new_month = "es.map(e=>`<button class=\"adb\" data-open=\"${esc(e.id)}\" style=\"background:${staffColor(e)}\">${e.time?fmtTime(e.time).replace(':00','')+' ':''}${esc(e.title)}</button>`).join('')}"
if old_month in html:
    html = html.replace(old_month, new_month, 1)
    print("OK: Month shows all")

# 4. Day navigation
old_nav = "if(S.calMode==='month')d.setMonth(d.getMonth()+n);else "
new_nav = "if(S.calMode==='month')d.setMonth(d.getMonth()+n);else if(S.calMode==='day')d.setDate(d.getDate()+n);else "
if old_nav in html:
    html = html.replace(old_nav, new_nav, 1)
    print("OK: Day nav")

# 5. Add day view renderer before week block
old_dispatch = "  let title,body;\n  if(S.calMode==='week'){"
new_dispatch = """  let title,body;
  if(S.calMode==='day'){
    const ds=iso(S.calDate);
    title=S.calDate.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});
    const evs=EZ.evs.filter(e=>e.date===ds);
    const allDay=evs.filter(e=>!e.time);
    const timed=evs.filter(e=>e.time&&!(e.endDate&&e.endDate>e.date));
    const spanBlocks=evs.filter(e=>e.time&&e.endDate&&e.endDate>e.date&&e.date===ds).map(function(e){
      var s=toMin(e.time),top=Math.max(0,(s-H0*60))*48/60,h=(H1-H0)*48-top;
      return '<button class="blk" data-open="'+esc(e.id)+'" style="top:'+top+'px;height:'+h+'px;left:1px;width:calc(100% - 2px);background:'+staffColor(e)+';border-radius:4px;z-index:2;overflow:hidden"><b>'+fmtTime(e.time)+'</b> '+esc(e.title)+'</button>';
    }).join('');
    const lanes=[];timed.forEach(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;let L=0;while(lanes[L]&&lanes[L]>s)L++;lanes[L]=en;e._l=L;});
    const n=Math.max(1,lanes.length);
    const blocks=timed.map(e=>{
      const s=toMin(e.time),en=e.end?toMin(e.end):s+60;
      const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);
      const w=100/n;
      return `<button class="blk" data-open="${esc(e.id)}" style="top:${top}px;height:${h}px;left:calc(${e._l*w}% + 2px);width:calc(${w}% - 4px);background:${staffColor(e)}"><b>${fmtTime(e.time)}</b> ${esc(e.title)}</button>`;
    }).join('');
    const adbRow=allDay.length?`<div class="wgrid" style="min-width:0"><div class="whead" style="font-size:11px;color:var(--muted)">all-day</div><div class="dcol" style="min-height:28px">${allDay.map(e=>`<button class="adb" data-open="${esc(e.id)}" style="background:${staffColor(e)}">${esc(e.title)}</button>`).join('')}</div></div>`:'';
    let nowl='';if(ds===TODAY){const nw=new Date();const m=nw.getHours()*60+nw.getMinutes();if(m>H0*60&&m<H1*60)nowl=`<div class="nowline" style="top:${(m-H0*60)*48/60}px"></div>`;}
    body=`${adbRow}<div class="wgrid" style="min-width:0"><div class="whead" style="font-size:11px;color:var(--muted)">Time</div><div class="dcol" style="width:100%">${[...Array(H1-H0)].map((_,k)=>`<div class="slot" data-slot="${ds}|${H0+k}" title="New appointment"></div>`).join('')}${blocks}${spanBlocks}${nowl}</div></div>`;
  } else if(S.calMode==='week'){"""
if old_dispatch in html:
    html = html.replace(old_dispatch, new_dispatch, 1)
    print("OK: Day view renderer")
else:
    print("MISS: dispatch")
    idx = html.find("let title,body")
    print(repr(html[idx:idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
