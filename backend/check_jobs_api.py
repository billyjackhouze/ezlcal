from pathlib import Path
src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
idx = src.find("@app.get(\"/jobs\")")
if idx < 0: idx = src.find("'/jobs'")
if idx < 0: idx = src.find('"/jobs"')
print(repr(src[max(0,idx-20):idx+400]))
