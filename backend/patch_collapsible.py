from pathlib import Path

f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
print(f"Size: {len(html)}, collapsible already: {'collapsible' in html}")

if "toggleBox" in html:
    print("Already patched")
else:
    # 1. CSS
    old = ".boxhead{padding:9px 14px;background:var(--side);border-bottom:1px solid var(--line);display:flex;gap:8px;align-items:center;flex-wrap:wrap}"
    new = (old +
        ".boxhead.collapsible{cursor:pointer;user-select:none}"
        ".boxhead.collapsible:hover{background:var(--hover)}"
        ".collapse-chevron{margin-left:auto;font-size:11px;transition:transform .2s;color:var(--sub)}"
        ".box.collapsed>.boxhead .collapse-chevron{transform:rotate(-90deg)}"
        ".box.collapsed>.collapsible-body{display:none}")
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: CSS")

    # 2. toggleBox function
    old = "window.toggleCalWho="
    new = ("window.toggleBox=function(id){var box=document.getElementById(id);if(box)box.classList.toggle('collapsed');};"
           "window.toggleCalWho=")
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: toggleBox fn")

    # 3. Contacts box
    old = '<div class="box"><div class="boxhead"><b>Contacts</b><span class="muted">${people.length}</span><span class="spacer"></span><button class="btn" style="height:26px;padding:0 9px;font-size:12px" onclick="openNewContact(${i})">+ Add contact</button></div><div style="overflow-x:auto"><table class="ctab">'
    new = '<div class="box" id="cbox_${i}"><div class="boxhead collapsible" onclick="toggleBox(\'cbox_\'+${i})"><b>Contacts</b><span class="muted">${people.length}</span><span class="spacer"></span><button class="btn" style="height:26px;padding:0 9px;font-size:12px" onclick="event.stopPropagation();openNewContact(${i})">+ Add contact</button><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body" style="overflow-x:auto"><table class="ctab">'
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: Contacts")

    # 4. Close contacts collapsible-body
    old = "</tbody></table></div></div>`:''"
    new = "</tbody></table></div></div></div>`:''"
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: Contacts close")

    # 5. Quotes box
    old = '<div class="box" id="qbox_${i}"><div class="boxhead"><b>Quotes</b><span class="spacer"></span></div><div class="empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
    new = '<div class="box" id="qbox_${i}"><div class="boxhead collapsible" onclick="toggleBox(\'qbox_\'+${i})"><b>Quotes</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
    assert old in html, f"Quotes not found"
    html = html.replace(old, new, 1)
    print("OK: Quotes")

    # 6. Jobs box
    old = '<div class="box" id="jbox_${i}"><div class="boxhead"><b>Jobs</b><span class="spacer"></span></div><div class="empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
    new = '<div class="box" id="jbox_${i}"><div class="boxhead collapsible" onclick="toggleBox(\'jbox_\'+${i})"><b>Jobs</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
    assert old in html, f"Jobs not found"
    html = html.replace(old, new, 1)
    print("OK: Jobs")

    # 7. Company family box
    old = '<div class="box"><div class="boxhead"><b>Company family</b><span class="muted">parent, children and grandchildren</span><span class="spacer"></span>'
    new = '<div class="box" id="fambox_${i}"><div class="boxhead collapsible" onclick="toggleBox(\'fambox_\'+${i})"><b>Company family</b><span class="muted">parent, children and grandchildren</span><span class="spacer"></span>'
    assert old in html
    html = html.replace(old, new, 1)

    old = '</span></div>\n        <div style="max-height:320px;overflow:auto">'
    new = '</span><span class="collapse-chevron">&#9662;</span></div>\n        <div class="collapsible-body" style="max-height:320px;overflow:auto">'
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: Company family")

    # 8. renderQJBox redirect to collapsible-body
    old = "function renderQJBox(box,data,isQuote){"
    new = "function renderQJBox(box,data,isQuote){var _body=box.querySelector('.collapsible-body');if(_body)box=_body;"
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: renderQJBox redirect")

    f.write_text(html, encoding="utf-8")
    Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
    print(f"Done: {len(html)} chars, collapsible count: {html.count('collapsible')}")
