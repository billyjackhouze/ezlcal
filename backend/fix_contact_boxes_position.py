from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")

# Remove the misplaced boxes (currently outside the template)
bad = ('<div class="box" id="cqbox_${i}"><div class="boxhead collapsible" data-toggle="cqbox_${i}"><b>Quotes</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
       '<div class="box" id="cjbox_${i}"><div class="boxhead collapsible" data-toggle="cjbox_${i}"><b>Jobs</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>')
assert bad in html, "bad boxes not found"
html = html.replace(bad, '', 1)
print("OK: removed misplaced boxes")

# Insert correctly inside the backtick template, before </section>
# The contact template ends with: </section><aside class="activity pane"><b>All activity</b>${timeline(evs)}</aside>`;
old = '</section><aside class="activity pane"><b>All activity</b>${timeline(evs)}</aside>`'
new = ('<div class="box" id="cqbox_${i}"><div class="boxhead collapsible" data-toggle="cqbox_${i}"><b>Quotes</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
       '<div class="box" id="cjbox_${i}"><div class="boxhead collapsible" data-toggle="cjbox_${i}"><b>Jobs</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
       '</section><aside class="activity pane"><b>All activity</b>${timeline(evs)}</aside>`')
assert old in html, "template end not found"
html = html.replace(old, new, 1)
print("OK: boxes inserted inside template")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
