from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

# Remove the </script><script> boundary between block 1 and block 2
old = "</script>\n<script>\nwindow.__start=function(D){"
new = "window.__start=function(D){"
if old in html:
    html = html.replace(old, new, 1)
    print("OK: merged script blocks")
else:
    print("MISS")
    # Try alternate
    old2 = "</script>\r\n<script>\r\nwindow.__start=function(D){"
    if old2 in html:
        html = html.replace(old2, new, 1)
        print("OK: merged (CRLF)")
    else:
        # Show what is around that area
        idx = html.find("window.__start=function(D)")
        print("Context:", repr(html[max(0,idx-30):idx+30]))

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
