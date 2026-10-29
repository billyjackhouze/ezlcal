from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

print("delegation exists:", "[data-toggle]" in html)
print("toggleBox exists:", "toggleBox" in html)

if "[data-toggle]" not in html:
    # Add event delegation after toggleBox definition
    old = "window.toggleBox=function(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');};"
    new = ("window.toggleBox=function(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');};"
           "document.addEventListener('click',function(e){"
           "var h=e.target.closest('[data-toggle]');"
           "if(h&&!e.target.closest('button')&&!e.target.closest('a')){"
           "var box=document.getElementById(h.dataset.toggle);"
           "if(box)box.classList.toggle('collapsed');}});")
    if old in html:
        html = html.replace(old, new, 1)
        print("OK: delegation added")
    else:
        # toggleBox may have different form - find it
        idx = html.find("toggleBox=function")
        print("toggleBox form:", repr(html[idx:idx+100]))
else:
    print("Already has delegation")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
