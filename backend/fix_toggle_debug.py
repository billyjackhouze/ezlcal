from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# The delegation fires on [data-toggle] elements
# but h.dataset.toggle gives the value - verify the listener uses the BOX id correctly
# Current: var box=document.getElementById(h.dataset.toggle)
# h.dataset.toggle = "cqbox_839" -> getElementById("cqbox_839") -> the .box div
# Then box.classList.toggle("collapsed") -> adds collapsed to .box
# CSS: .box.collapsed>.collapsible-body{display:none} -> should work

# Check if collapsed CSS is actually in the file
print("collapsed CSS:", ".box.collapsed>.collapsible-body{display:none}" in html)
print("collapsed chevron:", ".box.collapsed>.boxhead .collapse-chevron" in html)

# The real issue may be: renderQJBox replaces collapsible-body content
# with a new boxhead inside it - check
idx = html.find("box.innerHTML=`<div")
print(f"\nrenderQJBox innerHTML at {idx}:")
print(repr(html[idx:idx+200]))
