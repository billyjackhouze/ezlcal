from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix en calculation - toMin returns 0 for "00:00" which is falsy
# Use explicit null check instead of ||
old = 'var s=toMin(e._mdStart||e.time),en=toMin(e._mdEnd||(e.end||""))||s+60;'
new = 'var st=e._mdStart||e.time,et=e._mdEnd||(e.end||"");var s=toMin(st),en=et?toMin(et):s+60;if(en<=s)en=s+60;'
count = html.count(old)
print(f"Found {count}")
html = html.replace(old, new)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
