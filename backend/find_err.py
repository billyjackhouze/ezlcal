from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")
lines = html.split("\n")
print(f"Line 303: {repr(lines[302])}")
print(f"Line 302: {repr(lines[301])}")
print(f"Line 304: {repr(lines[303])}")
