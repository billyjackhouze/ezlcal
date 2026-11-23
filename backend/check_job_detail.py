from pathlib import Path
html = Path(r"C:\Apps\ezlcal\web\index.html").read_text(encoding="utf-8")
idx = html.find('class="qjdetail"')
print(repr(html[idx:idx+400]))
# Find toggleQJDetail function
idx2 = html.find("toggleQJDetail")
while idx2 >= 0:
    print(idx2, repr(html[idx2:idx2+100]))
    idx2 = html.find("toggleQJDetail", idx2+1)
    if idx2 > 100000: break
