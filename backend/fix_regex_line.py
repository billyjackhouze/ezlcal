from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find and remove the broken regex line
bad = "    const si=STF.findIndex(s=>s&&s[2]&&new RegExp(s[2].replace(/[.*+?^${}()|[\\]\\]/g,'\\'\\$&\\'),'i').test(e.createdBy));"
safe = "    const si=STF.findIndex(function(sx){return sx&&sx[2]&&e.createdBy.toLowerCase().indexOf(sx[2].toLowerCase())>=0;});"

count = html.count(bad)
print(f"Found {count} instances of broken regex line")
if count:
    html = html.replace(bad, safe)
    print("Fixed")
else:
    # Search by partial match
    import re
    matches = list(re.finditer(r"STF\.findIndex\(s=>s&&s\[2\]&&new RegExp", html))
    print(f"Found {len(matches)} RegExp findIndex calls")
    for m in matches:
        print(f"  at {m.start()}: {repr(html[m.start():m.start()+150])}")
        # Replace each one
    html = re.sub(
        r"STF\.findIndex\(s=>s&&s\[2\]&&new RegExp\([^)]+\)\.test\(e\.createdBy\)\)",
        "STF.findIndex(function(sx){return sx&&sx[2]&&e.createdBy.toLowerCase().indexOf(sx[2].toLowerCase())>=0;})",
        html
    )
    print("Replaced all RegExp findIndex calls")

Path(r"C:\Apps\ezlcal\backend\dist\index.html").write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
