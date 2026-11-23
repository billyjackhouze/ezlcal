from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find jobs table render
idx = html.find("Search jobs")
print("jobs section:", repr(html[idx:idx+400]))

# Find the API endpoint for jobs
idx2 = html.find("/api/accounts/")
while idx2 >= 0:
    print(idx2, repr(html[idx2:idx2+60]))
    idx2 = html.find("/api/accounts/", idx2+1)
    if idx2 > 80000: break
