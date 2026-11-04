from pathlib import Path
import subprocess
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print("Size:", len(html))
print("f_end_date:", "f_end_date" in html)
# Find the area around f_end_date
idx = html.find("f_end_date")
print("Context:", repr(html[idx-20:idx+150]))
