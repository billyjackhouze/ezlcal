from pathlib import Path
html = Path(r"C:\Apps\ezlcal\backend\dist\index.html").read_text(encoding="utf-8")

# Find where ACC rows are parsed/mapped
idx = html.find("IX.a.get(a[4])")
print("ACC row parse:", repr(html[max(0,idx-100):idx+200]))

# Find where individual account fields are accessed in display
idx2 = html.find("money(a[4])")
print("\nmoney(a[4]):", repr(html[max(0,idx2-100):idx2+100]))

# Find the family() function
idx3 = html.find("function family(")
if idx3 < 0: idx3 = html.find("family=function(")
if idx3 < 0: idx3 = html.find("const family=")
print("\nfamily func:", repr(html[idx3:idx3+200]))
