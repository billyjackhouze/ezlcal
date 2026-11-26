from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Find the conditional contacts box
idx = html.find("${people.length?`<div class=\"box\" id=\"cbox_")
end = html.find("</div></div>`:''}",  idx)
if idx < 0:
    print("MISS - trying alternate")
    idx = html.find('${people.length?`<div class="box" id="cbox_')
    end = html.find("</div></div>`:''}",  idx)

print("Found at:", idx, "end:", end)
print("Current:", repr(html[idx:idx+60]))
print("End:", repr(html[end:end+20]))

# Replace ${people.length?`...`:''}  with just the box (always shown)
# Remove the ternary wrapper
old_start = "${people.length?`"
old_end = "</div></div>`:''}"+"\n"

start_idx = html.find(old_start, idx)
end_idx = html.find(old_end, start_idx) + len(old_end)

old_block = html[start_idx:end_idx]
# New: always show, but add empty state inside tbody when no contacts
new_block = html[start_idx+len(old_start):end_idx-len(old_end)] + "\n"

if old_block:
    html = html[:start_idx] + new_block + html[end_idx:]
    print("OK: contacts box always shown")
else:
    print("MISS block")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
