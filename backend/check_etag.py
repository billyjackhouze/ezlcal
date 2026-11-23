from pathlib import Path
src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
idx = src.find("stamp")
print(repr(src[max(0,idx-50):idx+300]))
