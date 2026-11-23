from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find("function toggleQJDetail")
# Check what wraps it - is it inside a closure or global?
print("Before fn:", repr(html[max(0,idx-100):idx+20]))
# Check if it is inside a script tag or closure
script_start = html.rfind("<script>", 0, idx)
closure_start = html.rfind("(function(", 0, idx)
print(f"\nNearest <script>: {script_start}")
print(f"Nearest closure: {closure_start}")
print(f"toggleQJDetail at: {idx}")
print("Is inside closure:", closure_start > script_start)
