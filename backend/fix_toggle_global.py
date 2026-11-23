from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Add window.toggleQJDetail = toggleQJDetail after the function definition
old = "function toggleQJDetail(tr){"
# Find the end of the function
idx = html.find(old)
end = html.find("\nfunction ", idx+1)
fn_block = html[idx:end]
print("fn ends with:", repr(fn_block[-50:]))

# Add window assignment right after the closing brace
new = old  # keep the function as-is
# Insert window assignment after the function
insert_after = html[idx:end].rstrip()
new_block = insert_after + "\nwindow.toggleQJDetail=toggleQJDetail;\nwindow.filterQJTable=filterQJTable;\nwindow.filterMainQJTable=filterMainQJTable;\n"
html = html[:idx] + new_block + html[end:]
print("OK: exposed to window")

f.write_text(html, encoding="utf-8")

# Deploy
utf8nobom = "utf-8-sig"
import codecs
content = open(r"C:\Apps\ezlcal\web\index.html", encoding="utf-8").read()
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(content)
print("Deployed")
