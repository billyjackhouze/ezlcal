from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
print("already patched:", "_savedWho" in html)
if "_savedWho" not in html:
    old = "const S={view:'team',calMode:'week',calDate:new Date(),calWho:-1,"
    new = ("const _savedWho=localStorage.getItem('ezl_calWho');"
           "const _initWho=_savedWho!==null?+_savedWho:(EZ.meIdx>=0?EZ.meIdx:-1);"
           "const S={view:'team',calMode:'week',calDate:new Date(),calWho:_initWho,")
    assert old in html
    html = html.replace(old, new, 1)

    old2 = "window.pickCalWho=i=>{S.calWho=i;const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';render();};"
    new2 = "window.pickCalWho=i=>{S.calWho=i;try{localStorage.setItem('ezl_calWho',i);}catch(e){}const dd=document.getElementById('calwho-dd');if(dd)dd.style.display='none';render();};"
    assert old2 in html
    html = html.replace(old2, new2, 1)

    f.write_text(html, encoding="utf-8")
    Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
    print("Done")
