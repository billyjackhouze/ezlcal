from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# The contact detail is inside a template literal (backtick string)
# so ${i} SHOULD expand. But check - is the contact section in backticks?
# The renderQJBox writes to the collapsible-body child, so toggle needs to work on the box
# The issue: after renderQJBox runs, it replaces box content but box is already the collapsible-body
# So the boxhead with data-toggle is preserved. The toggle should work.
# Real issue: the boxes are ADDED to the DOM after render via renderQJBox
# but the event delegation is on document so it should still fire.
# Let's check if the id matches - the box id is set in JS via getElementById
# cqbox_${i} in a template literal WILL expand correctly.
# The data-toggle value must also expand - verify it does by checking template context

idx = html.find("if(k===\"c\"){")
print(f"contact section at: {idx}")
# Find the return statement  
ret_idx = html.find("return `<section", idx)
print(f"contact return at: {ret_idx}")
# Check if cqbox is in the backtick template
end_idx = html.find("</aside>`", ret_idx)
snippet = html[ret_idx:end_idx+10]
print(f"In backtick template: {'cqbox_$' in snippet}")
print(f"data-toggle in snippet: {'data-toggle' in snippet}")
print("Last 200 chars before aside:", repr(snippet[-300:-100]))
