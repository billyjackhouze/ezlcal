from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Replace K.c[conIdx] with a window-exposed version
# First expose K on window inside the boot closure
old_expose = "window.__IX=IX;"
new_expose = "window.__IX=IX;window.__K=K;"
if old_expose in html:
    html = html.replace(old_expose, new_expose, 1)
    print("OK: K exposed as window.__K")
else:
    # Try alternate - find where window.__ezl is set
    old2 = "window.__ezl="
    idx = html.find(old2)
    print(f"window.__ezl at {idx}: {repr(html[idx-20:idx+40])}")

# Fix loadContactQJ to use window.__K instead of K
old_fn = "var cid=K.c[conIdx];if(!cid)return;"
new_fn = "var _K=typeof K!=='undefined'?K:window.__K;var cid=_K&&_K.c?_K.c[conIdx]:null;if(!cid)return;"
if old_fn in html:
    html = html.replace(old_fn, new_fn, 1)
    print("OK: loadContactQJ uses window.__K fallback")
else:
    idx = html.find("loadContactQJ")
    print("MISS:", repr(html[idx:idx+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
