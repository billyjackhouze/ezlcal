from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print(f"Size: {len(html)} chars, {html.count(chr(10))} lines")
for term in ["catColor", "staffColor", "CATS=", "Personal", "createdBy", "m_edit", "Appointment colors", "Customer visit"]:
    idx = html.find(term)
    if idx >= 0:
        print(f"  {term} at {idx}: {repr(html[idx:idx+80])}")
    else:
        print(f"  {term}: NOT FOUND")
