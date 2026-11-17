from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find the lane algorithm and blocks rendering
# Current: timed events go through lane calc, then render as blocks
# We need multi-day events to also go through the lane calc

old = "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
new = (
    # Include multi-day start-day events in timed for lane calculation
    "const multiDay=evs.filter(e=>e.date===ds&&e.time&&e.endDate&&e.endDate>e.date);"
    "const timed=evs.filter(e=>e.date===ds&&e.time&&!(e.endDate&&e.endDate>e.date));"
    "const allTimed=[...timed,...multiDay];"
)
assert old in html
html = html.replace(old, new, 1)
print("OK: multiDay extracted")

# Change lanes calc to use allTimed
old_lanes = "const lanes=[];timed.forEach(e=>{"
new_lanes = "const lanes=[];allTimed.forEach(e=>{"
assert old_lanes in html
html = html.replace(old_lanes, new_lanes, 1)
print("OK: lanes uses allTimed")

# Change n= to use allTimed
old_n = "const n=Math.max(1,lanes.length);"
new_n = "const n=Math.max(1,lanes.length);"  # unchanged
print("OK: n unchanged")

# Change blocks render to use allTimed, with tall height for multi-day
old_blocks = "const blocks=timed.map(e=>{"
new_blocks = "const blocks=allTimed.map(e=>{"
assert old_blocks in html
html = html.replace(old_blocks, new_blocks, 1)
print("OK: blocks uses allTimed")

# Change block height: multi-day stretches to bottom, regular uses end time
old_height = "const top=Math.max(0,(s-H0*60))*48/60,h=Math.max(22,(en-s)*48/60);const w=100/n;"
new_height = "const top=Math.max(0,(s-H0*60))*48/60,h=e.endDate&&e.endDate>e.date?(H1-H0)*48-top:Math.max(22,(en-s)*48/60);const w=100/n;"
assert old_height in html
html = html.replace(old_height, new_height, 1)
print("OK: tall height for multi-day")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
