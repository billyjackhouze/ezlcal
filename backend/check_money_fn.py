from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find money function
idx = html.find("function money(")
if idx < 0: idx = html.find("const money=")
print("money():", repr(html[idx:idx+150]))

# Find quotes YTD display
idx2 = html.find("quotes YTD")
print("\nquotes display:", repr(html[max(0,idx2-20):idx2+200]))
