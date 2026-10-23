from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = "$('#calwho').onchange=e=>{S.calWho=+e.target.value;render()};"
new = """window.toggleCalWho=()=>{const dd=document.getElementById('calwho-dd');if(dd)dd.style.display=dd.style.display==='none'?'block':'none';};
  window.pickCalWho=i=>{S.calWho=i;const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';render();};
  document.addEventListener('click',e=>{if(!e.target.closest('.calwho-wrap')){const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';}},true);"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK: replaced onchange handler")
else:
    # Try without semicolon at end
    old2 = "$('#calwho').onchange=e=>{S.calWho=+e.target.value;render();}"
    if old2 in html:
        html = html.replace(old2, new, 1)
        print("OK: replaced (no trailing semicolon)")
    else:
        print("MISS - searching...")
        idx = html.find("calwho').onchange")
        if idx >= 0:
            print(repr(html[idx-5:idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
