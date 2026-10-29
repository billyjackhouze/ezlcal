from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = ("document.addEventListener('click',function(e){"
       "var h=e.target.closest('[data-toggle]');"
       "if(h&&!e.target.closest('button')&&!e.target.closest('a')){"
       "var box=document.getElementById(h.dataset.toggle);"
       "if(box)box.classList.toggle('collapsed');}});")
new = ("document.addEventListener('click',function(e){"
       "var h=e.target.closest('[data-toggle]');"
       "console.log('toggle click',h,h&&h.dataset.toggle);"
       "if(h&&!e.target.closest('button')&&!e.target.closest('a')){"
       "var box=document.getElementById(h.dataset.toggle);"
       "console.log('toggling box',box,box&&box.id);"
       "if(box)box.classList.toggle('collapsed');}});")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: debug added")
else:
    print("MISS")
    idx = html.find("data-toggle]')")
    print(repr(html[idx-80:idx+100]))

f.write_text(html, encoding="utf-8")
