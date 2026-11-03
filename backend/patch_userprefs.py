from pathlib import Path

# 1. Add columns to DB
import psycopg, os
from dotenv import load_dotenv
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    c.execute("ALTER TABLE app_users ADD COLUMN IF NOT EXISTS default_tab TEXT DEFAULT 'cal'")
    c.execute("ALTER TABLE app_users ADD COLUMN IF NOT EXISTS cal_default BOOLEAN DEFAULT TRUE")
    c.commit()
    cols = c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='app_users'").fetchall()
    print("app_users cols:", [r["column_name"] for r in cols])

# 2. Patch main.py - admin SELECT and prefs endpoint
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

if "default_tab" not in src:
    # Add to admin SELECT
    old = ("a.must_change, a.created_at, a.last_login, a.created_by\n"
           "               FROM app_users a LEFT JOIN staff s ON s.id =")
    new = ("a.must_change, a.created_at, a.last_login, a.created_by,\n"
           "                      coalesce(a.default_tab,'cal') as default_tab, coalesce(a.cal_default,true) as cal_default\n"
           "               FROM app_users a LEFT JOIN staff s ON s.id =")
    assert old in src, "admin SELECT not found"
    src = src.replace(old, new, 1)
    print("OK: admin SELECT")

    # Add prefs endpoint
    marker = "# ---------- global quotes and jobs ----------"
    ep = (
        "\n@app.put(\"/api/admin/users/{username}/prefs\")\n"
        "def set_user_prefs(username: str, body: dict, u: dict = Depends(admin_user)):\n"
        "    allowed = {'default_tab', 'cal_default'}\n"
        "    updates = {k: v for k, v in body.items() if k in allowed}\n"
        "    if not updates: raise HTTPException(400, 'No valid fields')\n"
        "    with pool.connection() as c:\n"
        "        for k, v in updates.items():\n"
        "            c.execute(f'UPDATE app_users SET {k}=%s WHERE username=%s', (v, username))\n"
        "        c.commit()\n"
        "    return {'ok': True}\n\n"
    )
    assert marker in src
    src = src.replace(marker, ep + marker, 1)
    print("OK: prefs endpoint")

    # Add to boot response
    old_boot = '"display_name", "must_change", "is_admin")'
    new_boot = '"display_name", "must_change", "is_admin", "default_tab", "cal_default")'
    if old_boot in src:
        src = src.replace(old_boot, new_boot, 1)
        print("OK: boot response")

    f.write_text(src, encoding="utf-8")
else:
    print("main.py already patched")

# 3. Patch index.html - add User Preferences section
f2 = Path(r"C:\Apps\ezlcal\backend\dist\index.html")
html = f2.read_text(encoding="utf-8")

if "user-prefs-panel" not in html:
    # Add box after staff color picker box
    old_box = '<div class="box" style="margin-top:16px"><div class="boxhead"><b>Staff Calendar Colors</b></div><div id="staff-color-picker" style="padding:10px 14px"></div></div>`'
    new_box = ('<div class="box" style="margin-top:16px"><div class="boxhead"><b>Staff Calendar Colors</b></div><div id="staff-color-picker" style="padding:10px 14px"></div></div>'
               '<div class="box" style="margin-top:16px"><div class="boxhead"><b>User Preferences</b><span class="muted" style="font-size:12px;margin-left:8px">Default tab and calendar view on login</span></div><div id="user-prefs-panel" style="overflow-x:auto"></div></div>`')
    assert old_box in html, "color box not found"
    html = html.replace(old_box, new_box, 1)
    print("OK: prefs box in HTML")

    # Add renderUserPrefs call
    old_raf = "requestAnimationFrame(()=>{const el=document.getElementById('staff-color-picker');if(el)renderStaffColorPicker(el);});"
    new_raf = (old_raf +
               "requestAnimationFrame(()=>renderUserPrefs(main,ADM));")
    assert old_raf in html
    html = html.replace(old_raf, new_raf, 1)
    print("OK: renderUserPrefs call")

    # Add renderUserPrefs function
    old_fn = "async function admCall(path,opt,okMsg){"
    new_fn = (
        "function renderUserPrefs(main,adm){"
        "var el=document.getElementById('user-prefs-panel');if(!el)return;"
        "var TABS=[['cal','Calendar'],['a','Accounts'],['c','Contacts'],['s','Staff'],['quotes','Quotes'],['jobs','Jobs'],['map','Map'],['team','Team']];"
        "var rows=(adm.users||[]).filter(function(u){return !u.disabled;}).map(function(u){"
        "var dt=u.default_tab||'cal';"
        "var cd=u.cal_default!==false;"
        "var opts=TABS.map(function(t){return '<option value=\"'+t[0]+'\"'+(dt===t[0]?' selected':'')+'>'+t[1]+'</option>';}).join('');"
        "return '<tr><td style=\"padding:7px 12px;font-size:13px\"><b>'+esc(u.display_name)+'</b></td>'"
        "+'<td style=\"padding:7px 12px\"><select style=\"font-size:12px\" onchange=\"saveUserPref(\\''+esc(u.username)+'\\',\\'default_tab\\',this.value)\">'+opts+'</select></td>'"
        "+'<td style=\"padding:7px 12px\"><label style=\"display:flex;gap:8px;align-items:center;font-size:12px;cursor:pointer\"><input type=\"checkbox\"'+(cd?' checked':'')+' onchange=\"saveUserPref(\\''+esc(u.username)+'\\',\\'cal_default\\',this.checked)\">Default to own calendar</label></td></tr>';"
        "}).join('');"
        "el.innerHTML='<table style=\"width:100%;border-collapse:collapse\"><thead><tr>"
        "<th style=\"text-align:left;font-size:12px;color:var(--sub);padding:4px 12px\">User</th>"
        "<th style=\"text-align:left;font-size:12px;color:var(--sub);padding:4px 12px\">Default tab</th>"
        "<th style=\"text-align:left;font-size:12px;color:var(--sub);padding:4px 12px\">Calendar</th>"
        "</tr></thead><tbody>'+rows+'</tbody></table>';}"
        "async function saveUserPref(username,key,val){"
        "await admCall('/admin/users/'+encodeURIComponent(username)+'/prefs',{method:'PUT',body:JSON.stringify({[key]:val})},'Saved');}"
        "async function admCall(path,opt,okMsg){"
    )
    assert old_fn in html
    html = html.replace(old_fn, new_fn, 1)
    print("OK: renderUserPrefs function")

    # Apply default_tab on boot
    old_view = "const _defTab=EZ.user.default_tab||'cal';"
    if old_view not in html:
        old_s = "const S={view:'team',calMode:'week',calDate:new Date(),calWho:_initWho,"
        new_s = "const _defTab=EZ.user.default_tab||'cal';const S={view:_defTab,calMode:'week',calDate:new Date(),calWho:_initWho,"
        if old_s in html:
            html = html.replace(old_s, new_s, 1)
            print("OK: default_tab on boot")
        old_s2 = "const S={view:'team',calMode:'week',calDate:new Date(),calWho:_initWho,"
        # already replaced above

    f2.write_text(html, encoding="utf-8")
    Path(r"C:\Apps\ezlcal\web\index.html").write_text(html, encoding="utf-8")
    print("OK: HTML saved")
else:
    print("HTML already patched")
