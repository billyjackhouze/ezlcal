from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find the global Jobs tab - how does it render the list
idx = html.find("calMode==='jobs'")
if idx < 0: idx = html.find("S.tab==='jobs'")
if idx < 0: idx = html.find("tab===\"jobs\"")
print("jobs tab handler:", repr(html[max(0,idx-30):idx+400]))

# Find where /api/jobs is called (global jobs list)
idx2 = html.find("api/jobs")
if idx2 < 0: idx2 = html.find("/api/jobs")
print("\napi/jobs:", repr(html[max(0,idx2-50):idx2+200]))
