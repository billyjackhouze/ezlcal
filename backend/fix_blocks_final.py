from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix 1: Remove multiDay from the week view - change blocks to use only timed
old = "const blocks=allTimed.map(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;"
new = "const blocks=timed.map(e=>{const s=toMin(e.time),en=e.end?toMin(e.end):s+60;"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: blocks uses timed only")

# Fix 2: multiDay still defined but not needed - leave it harmless
# Check what the blocks render outputs - find ${blocks} and ${spanBlocks} in week dcol
idx = html.find("${blocks}${spanBlocks}")
if idx < 0: idx = html.find("${blocks}")
print("blocks in template:", repr(html[max(0,idx-20):idx+60]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
