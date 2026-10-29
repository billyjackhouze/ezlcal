from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
print(f"Size: {len(html)}, loadContactQJ: {'loadContactQJ' in html}")

if "loadContactQJ" not in html:
    # 1. Add Q/J boxes to contact detail (before the closing </section>)
    old = "</section><aside class=\"activity pane\"><b>All activity</b>${timeline(evs)}</aside>`;\n  }"
    new = ('<div class="box" id="cqbox_${i}"><div class="boxhead collapsible" data-toggle="cqbox_${i}"><b>Quotes</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
           '<div class="box" id="cjbox_${i}"><div class="boxhead collapsible" data-toggle="cjbox_${i}"><b>Jobs</b><span class="spacer"></span><span class="collapse-chevron">&#9662;</span></div><div class="collapsible-body empty muted" style="font-size:12px;padding:12px 16px">Loading\u2026</div></div>'
           "</section><aside class=\"activity pane\"><b>All activity</b>${timeline(evs)}</aside>`;\n  }")
    assert old in html
    html = html.replace(old, new, 1)
    print("OK: Q/J boxes added")

    # 2. Add loadContactQJ function before loadQuotesJobs
    old_fn = "function loadQuotesJobs(acctIdx){"
    new_fn = ("function loadContactQJ(conIdx){"
        "var cid=K.c[conIdx];if(!cid)return;"
        "['q','j'].forEach(function(t){"
        "var box=document.getElementById(t==='q'?'cqbox_'+conIdx:'cjbox_'+conIdx);"
        "if(!box)return;"
        "EZ.api('/contacts/'+encodeURIComponent(cid)+'/'+(t==='q'?'quotes':'jobs')).then(function(r){"
        "if(!r||!r.ok){var b=box.querySelector('.collapsible-body');if(b)b.innerHTML='<div style=\"padding:10px 14px\" class=\"muted\">Could not load</div>';return;}"
        "return r.json().then(function(data){renderQJBox(box,data,t==='q');});"
        "}).catch(function(){});});"
        "}"
        "function loadQuotesJobs(acctIdx){")
    assert old_fn in html
    html = html.replace(old_fn, new_fn, 1)
    print("OK: loadContactQJ function added")

    # 3. Add trigger after account trigger
    old_trig = "if(k==='a'&&sel>=0)requestAnimationFrame(()=>requestAnimationFrame(()=>loadQuotesJobs(sel)));"
    new_trig = ("if(k==='a'&&sel>=0)requestAnimationFrame(()=>requestAnimationFrame(()=>loadQuotesJobs(sel)));"
                "if(k==='c'&&sel>=0)requestAnimationFrame(()=>requestAnimationFrame(()=>loadContactQJ(sel)));")
    assert old_trig in html
    html = html.replace(old_trig, new_trig, 1)
    print("OK: trigger added")
else:
    print("Already patched")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
