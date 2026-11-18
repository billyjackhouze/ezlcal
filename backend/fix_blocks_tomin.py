from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix blocks.map to use _mdStart/_mdEnd
old = ("const blocks=[...timed,...mdSpans].map(e=>{\n"
       "      const s=toMin(e.time),en=e.end?toMin(e.end):s+60;\n"
       "      const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);\n"
       "      const w=100/n;")
new = ("const blocks=[...timed,...mdSpans].map(e=>{\n"
       "      const s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||''))||s+60;\n"
       "      const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);\n"
       "      const w=100/n;")
if old in html:
    html = html.replace(old, new, 1)
    print("OK: blocks.map uses _mdStart/_mdEnd")
else:
    print("MISS")
    idx = html.find("const blocks=[...timed,...mdSpans]")
    print(repr(html[idx:idx+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
