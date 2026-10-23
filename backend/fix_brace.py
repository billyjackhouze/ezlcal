from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
old = "\nrender();\n};\n</script>"
new = "\nrender();\n</script>"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: removed extra brace")
else:
    print("MISS - trying alternate")
    old2 = "render();\n};"
    if old2 in html:
        html = html.replace(old2, "render();", 1)
        print("OK: removed via alternate")
    else:
        print("NOT FOUND")
f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
