from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find the broken area around line 630 col 287
# Look for the orphaned '' that broke the template
idx = html.find("''${blocks}${spanBlocks}")
if idx >= 0:
    print("Found broken pattern at:", idx)
    old = "''${blocks}${spanBlocks}"
    new = "${blocks}${spanBlocks}"
    html = html.replace(old, new, 1)
    print("OK: fixed")
else:
    # Find other patterns
    idx2 = html.find("join('')}''")
    idx3 = html.find("''${nowl}")
    idx4 = html.find("join('')}${blocks}")
    print("join('')}'':", idx2)
    print("''${nowl}:", idx3)  
    print("join('')}${blocks}:", idx4)
    if idx2 >= 0:
        print(repr(html[idx2-50:idx2+100]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
