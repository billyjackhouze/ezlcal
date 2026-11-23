from pathlib import Path
src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
# Find the exact SELECT and array construction
idx = src.find("SELECT a.id, a.name")
print("Query:", repr(src[idx:idx+600]))
idx2 = src.find("[a[\"id\"], a[\"name\"]")
if idx2 < 0: idx2 = src.find("float(a[\"sales_ytd\"])")
print("\nArray build:", repr(src[max(0,idx2-50):idx2+200]))
