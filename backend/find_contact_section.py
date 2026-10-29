from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
# Find cqbox in context
idx = html.find('id="cqbox_${i}"')
print(f"cqbox at {idx}")
# What comes 200 chars before
print("Before:", repr(html[idx-200:idx]))
# What type of string context - look for surrounding backtick
chunk = html[max(0,idx-500):idx+300]
bt = chunk.rfind("`")
sq = chunk.rfind("'")
dq = chunk.rfind('"', 0, len(chunk)-50)
print(f"Last backtick before: {bt}, last single-quote: {sq}")
print("Context char at bt:", repr(chunk[bt:bt+20]))
