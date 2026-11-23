from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find how accounts array is parsed - look for EZ.accs or similar
for term in ["EZ.accs", "accs=", "ACC=", "a[5]", "a[6]", "salesYtd", "sales_y", "YTD", "ytd"]:
    idx = html.find(term)
    if idx >= 0:
        print(f"{term}: {repr(html[max(0,idx-30):idx+80])}")
