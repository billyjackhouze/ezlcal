from pathlib import Path
src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
# Find the map endpoint
idx = src.find("518")
# Get lines 510-540
lines = src.split("\n")
for i, l in enumerate(lines[510:545], start=511):
    print(f"{i}: {l}")
