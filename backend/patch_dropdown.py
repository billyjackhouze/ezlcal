from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = """const who=`<select id="calwho" class="btn" aria-label="Whose calendar">${['<option value="-1">Everyone</option>'].concat(STF.map((s,i)=>`<option value="${i}" ${S.calWho===i?'selected':''}>${esc(s[0])}</option>`)).join('')}</select>`;"""

new = """const _swc=i=>{if(i<0)return '#888';const n=STF[i]?STF[i][0]||'':'';if(/tpalmer|trey/i.test(n))return '#e53935';if(/tgreen|^tim/i.test(n))return '#2e7d32';if(/goodwin|jesse/i.test(n))return '#1565c0';if(/jvela|joey|joseph/i.test(n))return '#00796b';return '#5f6b7a';};
  const _swn=S.calWho<0?'Everyone':esc(STF[S.calWho]?STF[S.calWho][0]:'');
  const _swdot=S.calWho<0?'':`<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${_swc(S.calWho)};margin-right:5px;vertical-align:middle"></span>`;
  const who=`<div class="calwho-wrap" style="position:relative;display:inline-block">
    <button class="btn" id="calwho-btn" onclick="toggleCalWho()" style="min-width:130px;text-align:left">${_swdot}${_swn} \u25be</button>
    <div id="calwho-dd" style="display:none;position:absolute;top:100%;left:0;z-index:999;background:var(--card);border:1px solid var(--border);border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.15);min-width:160px;padding:4px 0;margin-top:2px">
      <button class="calwho-opt" onclick="pickCalWho(-1)" style="display:flex;align-items:center;gap:8px;width:100%;padding:7px 12px;border:0;background:${S.calWho===-1?'var(--hover)':'none'};cursor:pointer;font-size:13px;text-align:left"><span style="width:8px;height:8px;border-radius:50%;background:#888;flex:0 0 8px"></span>Everyone</button>
      ${STF.map((s,i)=>`<button class="calwho-opt" onclick="pickCalWho(${i})" style="display:flex;align-items:center;gap:8px;width:100%;padding:7px 12px;border:0;background:${S.calWho===i?'var(--hover)':'none'};cursor:pointer;font-size:13px;text-align:left"><span style="width:8px;height:8px;border-radius:50%;background:${_swc(i)};flex:0 0 8px"></span>${esc(s[0])}</button>`).join('')}
    </div>
  </div>`;"""

old2 = "$('#calwho').onchange=e=>{S.calWho=+e.target.value;render()};"
new2 = """window.toggleCalWho=()=>{const dd=document.getElementById('calwho-dd');if(dd)dd.style.display=dd.style.display==='none'?'block':'none';};
  window.pickCalWho=i=>{S.calWho=i;const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';render();};
  document.addEventListener('click',e=>{if(!e.target.closest('.calwho-wrap')){const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';}},true);"""

changes = 0
for o, n in [(old, new), (old2, new2)]:
    if o in html:
        html = html.replace(o, n, 1)
        changes += 1
        print(f"OK ({changes})")
    else:
        print(f"MISS: {repr(o[:60])}")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print(f"Done: {changes} changes")
