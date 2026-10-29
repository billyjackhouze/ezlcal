from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# The issue: e.target.closest('[data-toggle]') works on the boxhead div itself
# but the chevron span and text inside also need to bubble up correctly
# closest() should handle this - but let's verify the delegation is actually firing
# by also handling clicks on children of [data-toggle] elements

# Check current delegation
idx = html.find("data-toggle]')")
print(f"delegation at {idx}:", repr(html[idx-100:idx+150]))
