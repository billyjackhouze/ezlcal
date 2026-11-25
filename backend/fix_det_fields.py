from pathlib import Path
f = Path(r"C:\Apps\ezlcal\web\index.html")
html = f.read_text(encoding="utf-8")

old = """r.enduser_ref?`<span><b>End User Ref:</b> ${r.enduser_ref}</span>`:'',
    ].filter(Boolean).jo"""

new = """r.enduser_ref?`<span><b>End User Ref:</b> ${r.enduser_ref}</span>`:'',
      (r.billing_address||r.billing_city)?`<span><b>Ship To:</b> ${[r.billing_address,r.billing_city,r.billing_state,r.billing_zip].filter(Boolean).join(', ')}</span>`:'',
    ].filter(Boolean).jo"""

if old in html:
    html = html.replace(old, new)
    print("OK: added billing address — found", html.count("Ship To:"), "instances")
else:
    print("MISS")

f.write_text(html, encoding="utf-8")
open(r"C:\Apps\ezlcal\backend\dist\index.html", "w", encoding="utf-8").write(html)
print("Deployed")
