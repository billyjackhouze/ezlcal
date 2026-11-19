from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

old = "join('')}${${blocks}${spanBlocks}${nowl}</div></div>`;"
new = "join('')}${blocks}${spanBlocks}${nowl}</div></div>`;"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: syntax fixed")
else:
    print("MISS - checking area")
    idx = html.find("join('')}$")
    while idx >= 0:
        print(idx, repr(html[idx:idx+60]))
        idx = html.find("join('')}$", idx+1)
        if idx > 52000: break

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
