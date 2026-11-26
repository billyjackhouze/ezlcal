from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Find where toggleQJDetail is assigned to window (in first block)
idx = html.find("window.toggleQJDetail=toggleQJDetail;")
print("toggleQJDetail assignment at:", idx)
print("Context:", repr(html[max(0,idx-50):idx+100]))
