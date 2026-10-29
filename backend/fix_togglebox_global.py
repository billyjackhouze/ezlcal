from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove the window.toggleBox= assignment (inside boot closure)
old_assign = "window.toggleBox=function(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');};"
if old_assign in html:
    html = html.replace(old_assign, "", 1)
    print("OK: removed window.toggleBox from closure")
else:
    print("MISS: window.toggleBox not found")
    idx = html.find("toggleBox")
    print(repr(html[idx:idx+100]))

# Add as a true top-level function declaration before </script>
old_end = "\nrender();\n</script>"
new_end = "\nrender();\n</script>"
# Find the script tag end and insert before it
old_script_end = "render();\n</script>"
new_script_end = "render();\n}\nfunction toggleBox(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');}\n</script>"

# Actually - just add it as a separate script block before </body>
old_body = "</body>\n</html>"
new_body = ('<script>function toggleBox(id){var box=document.getElementById(id);if(box)box.classList.toggle("collapsed");}</script>'
            "</body>\n</html>")
if old_body in html:
    html = html.replace(old_body, new_body, 1)
    print("OK: toggleBox added as global in separate script block")
else:
    print("MISS: </body> not found")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
