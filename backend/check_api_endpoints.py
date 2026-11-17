from pathlib import Path
src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
lines = src.split("\n")

# Show lines 350-510 (quotes/jobs API section)
for i, l in enumerate(lines[348:512], start=349):
    print(f"{i}: {l}")
