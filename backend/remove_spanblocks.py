from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Find and check spanBlocks
idx = html.find("spanBlocks")
print("spanBlocks at:", idx, repr(html[idx:idx+100]))

# Remove the entire spanBlocks variable and its use
html = re.sub(r"const spanBlocks=[^;]+;", "", html)
html = re.sub(r"\$\{spanBlocks\}", "", html)
print("spanBlocks remaining:", "spanBlocks" in html)

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
