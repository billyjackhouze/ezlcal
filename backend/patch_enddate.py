from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f.read_text(encoding="utf-8")
print("end_date in file:", "f_end_date" in html)
print("endDate in file:", "endDate" in html)

if "f_end_date" not in html:
    # Add end date field after end time input
    old = 'id="f_end" value="${e.end||\'\'}" aria-label="End time" ${e.time?\'\':\' disabled\'}>'
    new = ('id="f_end" value="${e.end||\'\'}" aria-label="End time" ${e.time?\'\':\' disabled\'}>'
           '<input type="date" id="f_end_date" value="${e.endDate||\'\'}" '
           'title="End date" placeholder="End date" aria-label="End date" style="margin-left:4px">')
    if old in html:
        html = html.replace(old, new, 1)
        print("OK: end date field added")
    else:
        print("MISS: f_end not found")
        idx = html.find("f_end")
        print(repr(html[idx:idx+100]))

if "endDate" not in html:
    # Add to fromServer
    old_from = "time:e.time||'',end:e.end||'',allDay:!e.time"
    new_from = "time:e.time||'',end:e.end||'',endDate:e.endDate||'',allDay:!e.time"
    if old_from in html:
        html = html.replace(old_from, new_from, 1)
        print("OK: fromServer endDate")

    # Add to toServer
    old_to = "time:e.time||'',end:e.end||'',cat:e.cat"
    new_to = "time:e.time||'',end:e.end||'',endDate:e.endDate||'',cat:e.cat"
    if old_to in html:
        html = html.replace(old_to, new_to, 1)
        print("OK: toServer endDate")

    # Add to sync
    old_sync = "e.end=all?'':$('#f_end').value;"
    new_sync = "e.end=all?'':$('#f_end').value;e.endDate=(function(){var d=$('#f_end_date');return d?d.value||'':'';})()"
    if old_sync in html:
        html = html.replace(old_sync, new_sync, 1)
        print("OK: sync endDate")

    # seed
    old_seed = "e.end=e.end||'';e.allDay=!e.time;seedById"
    new_seed = "e.end=e.end||'';e.endDate=e.endDate||'';e.allDay=!e.time;seedById"
    if old_seed in html:
        html = html.replace(old_seed, new_seed, 1)
        print("OK: seed endDate")

    # month view
    old_month = "const es=evs.filter(e=>e.date===ds);"
    if old_month in html:
        html = html.replace(old_month, "const es=evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds);", 1)
        print("OK: month view")

    # week allday
    old_week = "evs.filter(e=>e.date===ds&&!e.time).map"
    if old_week in html:
        html = html.replace(old_week, "evs.filter(e=>e.date<=ds&&(e.endDate||e.date)>=ds&&!e.time).map", 1)
        print("OK: week allday")

f.write_text(html, encoding="utf-8")
Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
print("Done", len(html))
