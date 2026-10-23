from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print(f"Size: {len(html)}")
idx = html.find("calwho")
while idx >= 0:
    print(f"  at {idx}: {repr(html[idx:idx+80])}")
    idx = html.find("calwho", idx+1)
    if idx > 200000: break
