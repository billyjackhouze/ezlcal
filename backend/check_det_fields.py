from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
# Find the det array build
idx = html.find("const det=[")
end = html.find("].filter(Boolean)", idx)
print("Current det fields:")
print(repr(html[idx:end+20]))
