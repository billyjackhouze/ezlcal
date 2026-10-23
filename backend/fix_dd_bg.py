from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
old = "background:${S.calWho===i?'var(--hover)':'none'};cursor:pointer"
new = "background:${S.calWho===i?'var(--hover)':'var(--card)'};cursor:pointer"
count = html.count(old)
html = html.replace(old, new)
old2 = "background:${S.calWho===-1?'var(--hover)':'none'};cursor:pointer"
new2 = "background:${S.calWho===-1?'var(--hover)':'var(--card)'};cursor:pointer"
html = html.replace(old2, new2)
print(f"Fixed {count+1} backgrounds")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
