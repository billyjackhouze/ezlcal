from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
print(f"Size: {len(html)}")
for term in ["staffColor", "_staffColorByName", "DEFAULT_STAFF_COLORS", "00695c", "6a1b9a", "createdBy", "scc_"]:
    idx = html.find(term)
    print(f"  {term}: {'at '+str(idx)+': '+repr(html[idx:idx+80]) if idx>=0 else 'NOT FOUND'}")
