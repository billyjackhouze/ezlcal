from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")

funcs = ["openNewContact", "openNewCompany", "toggleBox", "filterQJTable", "filterMainQJTable"]
closure_start = html.rfind("(function(", 0, html.find("function openNewContact"))

for fn in funcs:
    idx = html.find(f"function {fn}")
    if idx < 0:
        print(f"{fn}: NOT FOUND as function def")
        continue
    nearest_closure = html.rfind("(function(", 0, idx)
    in_closure = nearest_closure == closure_start
    # Check if window.X is assigned
    has_window = f"window.{fn}" in html
    print(f"{fn}: in_closure={in_closure}, window_assigned={has_window}")
