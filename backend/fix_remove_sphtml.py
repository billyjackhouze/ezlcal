from pathlib import Path
import re
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove the entire _spans/_sphtml block
old_spans = html[html.find("var _sphtml=''"):html.find("body=`<div class=\"week\" id=\"wk\"")]
print("Removing:", len(old_spans), "chars")
print("Preview:", repr(old_spans[:100]))

html = html.replace(old_spans, "", 1)

# Also simplify the body assembly to remove _sphtml reference
old_body = "body=`<div class=\"week\" id=\"wk\" style=\"position:relative\">${g}${_sphtml?'<div style=\"position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none\">'+_sphtml+'</div>':''}</div></div>`;"
new_body = "body=`<div class=\"week\" id=\"wk\">${g}</div></div>`;"
if old_body in html:
    html = html.replace(old_body, new_body, 1)
    print("OK: body simplified")
else:
    print("MISS body - checking")
    idx = html.find("body=`<div class=\"week\"")
    print(repr(html[idx:idx+150]))

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
