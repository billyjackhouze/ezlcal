from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and check what f_end_date looks like
idx = html.find("f_end_date")
print("Context:", repr(html[idx-20:idx+200]))

# Remove the broken end date field entirely and re-add it cleanly
import re
# Remove the f_end_date input (whatever form it's in)
html = re.sub(r'<input type="date" id="f_end_date"[^>]*>', '', html)
print("Removed f_end_date, still present:", "f_end_date" in html)

# Re-add it in the correct place with safe quoting
# The surrounding template uses backticks, so ${} is fine
# But single quotes inside the value attr need escaping
old = 'id="f_end" value="${e.end||\'\'}" aria-label="End time" ${e.time?\'\':\'disabled\'}>'
print("old found:", old in html)

# Try finding it differently
idx2 = html.find('"f_end"')
chunk = html[idx2:idx2+80]
print("f_end chunk:", repr(chunk))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
