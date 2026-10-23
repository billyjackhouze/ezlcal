from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find the leftover _staffColorByName call and the full old _swc tail
bad = "return _staffColorByName(STF[i]?STF[i][0]||'':''  ,i);};"
# Try exact
idx = html.find("return _staffColorByName")
if idx >= 0:
    end = html.index(";", html.index(");", idx))+1
    print(f"Found leftover at {idx}: {repr(html[idx:end])}")
    html = html[:idx] + html[end:]
    print("Removed leftover")
else:
    print("Not found by exact - searching broader")
    idx = html.find("staffColorByName")
    end = html.index(";", html.index(");", idx))+1
    print(f"Found at {idx}: {repr(html[idx:end])}")
    html = html[:idx] + html[end:]
    print("Removed")

print("staffColorByName remaining:", "staffColorByName" in html)
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
