from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Replace data-toggle with direct onclick on all collapsible boxheads
import re

# Replace data-toggle="X" with onclick="toggleBox('X')" on boxhead divs
def replace_toggle(m):
    val = m.group(1)
    return f'onclick="toggleBox(\'{val}\')"'

old_html = html
html = re.sub(r'data-toggle="([^"]+)"', replace_toggle, html)
count = old_html.count('data-toggle=') - html.count('data-toggle=')
print(f"Replaced {count} data-toggle attrs with onclick")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done")
