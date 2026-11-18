from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Fix mdSpans height calc - last day should end at end_time not H1
# Current: _mdEnd:isLast?(e.end||e.time):(H1+':00')
# Problem: H1 is 21 (9pm) not midnight, so middle days end at 9pm not midnight
# Fix: use '23:59' for end of day and correct last day end time

old = ("_mdStart:isFirst?e.time:(H0+':00'),"
       "_mdEnd:isLast?(e.end||e.time):(H1+':00')")
new = ("_mdStart:isFirst?e.time:'00:00',"
       "_mdEnd:isLast?(e.end||e.time):'23:59'")

count = html.count(old)
print(f"Found {count} occurrences")
html = html.replace(old, new)
print("OK: midnight boundaries fixed")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
