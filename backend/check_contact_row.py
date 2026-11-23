from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("Sales YTD</th><th")
# Get the tbody render after the header
idx2 = html.find("<tbody>", idx)
print(repr(html[idx2:idx2+500]))
