from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

# Find jobs section
idx = html.find("Search jobs")
print("jobs section:", repr(html[idx:idx+600]))

# Find job row template
idx2 = html.find("job_number")
if idx2 < 0: idx2 = html.find("job_date")
print("\njob row:", repr(html[max(0,idx2-50):idx2+200]))

# Find jobs API call
idx3 = html.find("/jobs")
while idx3 >= 0:
    print(idx3, repr(html[max(0,idx3-30):idx3+60]))
    idx3 = html.find("/jobs", idx3+1)
    if idx3 > 80000: break
