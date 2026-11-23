from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find the Jobs tab render - look for where tab=jobs is handled
idx = html.find("tab==='job'")
if idx < 0: idx = html.find("'jobs'")
print("Jobs tab:", repr(html[max(0,idx-50):idx+300]))

# Find renderQJ function
idx2 = html.find("function renderQJ")
if idx2 < 0: idx2 = html.find("renderQJ")
print("\nrenderQJ:", repr(html[idx2:idx2+200]))
