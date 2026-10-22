content = '''import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request, ssl
from datetime import datetime, timedelta
from pathlib import Path
import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

UUID_RE = re.compile(r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$")
PAGE = 1000
OVERLAP = timedelta(minutes=2)
LAYOUTS = {"accounts":"API_CRM_Accounts","contacts":"API_BUYER","links":"API_CRM_BuyerAccount","offices":"CRM_AccountOffice"}
TS_FIELD = {"accounts":"z_Modification_Time","contacts":"z_Modification_Time","links":None,"offices":"z_ModificationTimestamp"}
TYPE_CODES = {"customer":"C","enduser":"U","end user":"U","engref":"G","engineering":"G","engineering company":"G"}

def s(v): return "" if v is None else str(v).strip().replace(chr(0),"")
def num(v):
    try: return float(v or 0)
    except: return 0.0
def day(v):
    v=s(v)[:10]; return v if re.match(r"^\d{4}-\d{2}-\d{2}$",v) else None
def key(v):
    v=s(v).upper(); return v if UUID_RE.match(v) else ""
def type_codes(v):
    out={TYPE_CODES.get(t.strip().lower(),"") for t in re.split(r"[\r\n]+",s(v)) if t.strip()}
    return "".join(sorted(c for c in out if c))
def fm_ts(dt): return dt.strftime("%m/%d/%Y %H:%M:%S")

def _cfg():
    host=os.environ.get("FM_HOST","fms26.alamark.com").strip().rstrip("/")
    if not host.startswith("http"): host="https://"+host
    db=os.environ.get("FM_DB","ez-line")
    user=os.environ.get("FM_USER"); pw=os.environ.get("FM_PASSWORD")
    if not user or not pw: sys.exit("FM_USER/FM_PASSWORD not set")
    return host,db,user,pw

def _login(host,db,user,pw):
    import base64
    url=f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions"
    b64=base64.b64encode(f"{user}:{pw}".encode()).decode()
    req=urllib.request.Request(url,method="POST",data=b"{}",headers={"Authorization":f"Basic {b64}","Content-Type":"application/json"})
    ctx=ssl.create_default_context()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=30,context=ctx) as r:
                return json.loads(r.read())["response"]["token"]
        except urllib.error.HTTPError as e:
            body=e.read().decode("utf-8","replace")[:400]
            if attempt==2: sys.exit(f"FM login failed ({e.code}): {body}")
        time.sleep(2*(attempt+1))

def _logout(host,db,token):
    url=f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions/{token}"
    req=urllib.request.Request(url,method="DELETE",headers={"Authorization":f"Bearer {token}"})
    try: urllib.request.urlopen(req,timeout=10,context=ssl.create_default_context())
    except: pass

def _get_page(host,db,token,layout,offset,limit):
    url=(f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}"
         f"/layouts/{urllib.parse.quote(layout)}/records?_offset={offset}&_limit={limit}")
    req=urllib.request.Request(url,headers={"Authorization":f"Bearer {token}"})
    ctx=ssl.create_default_context()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=120,context=ctx) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body=e.read().decode("utf-8","replace")[:400]
            if attempt==2: raise SystemExit(f"FM error {e.code} for {layout}: {body}")
        time.sleep(2*(attempt+1))
    return {}

def _find(host,db,token,layout,ts_field,since):
    url=(f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}"
         f"/layouts/{urllib.parse.quote(layout)}/_find")
    ctx=ssl.create_default_context(); rows=[]; offset=1
    while True:
        body=json.dumps({"query":[{ts_field:f">={fm_ts(since - OVERLAP)}"],"limit":PAGE,"offset":offset}).encode()
        req=urllib.request.Request(url,method="POST",data=body,
            headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=120,context=ctx) as r:
                data=json.loads(r.read())
        except urllib.error.HTTPError as e:
            err=e.read().decode("utf-8","replace")
            if e.code==401 or chr(34)+"401"+chr(34) in err: break
            raise SystemExit(f"FM find error {e.code}: {err[:400]}")
        records=data.get("response",{}).get("data",[])
        for rec in records: rows.append(rec.get("fieldData",{}))
        if len(records)<PAGE: break
        offset+=PAGE
    return rows

def fetch_full(kind,token,host,db):
    rows,offset=[],1
    while True:
        data=_get_page(host,db,token,LAYOUTS[kind],offset,PAGE)
        records=data.get("response",{}).get("data",[])
        for rec in records: rows.append(rec.get("fieldData",{}))
        if len(records)<PAGE: break
        offset+=PAGE
    return rows

def fetch_delta(kind,token,host,db,since):
    if TS_FIELD[kind] is None: return fetch_full(kind,token,host,db)
    return _find(host,db,token,LAYOUTS[kind],TS_FIELD[kind],since)

def ensure_watermarks(c):
    c.execute("CREATE TABLE IF NOT EXISTS sync_watermarks (kind TEXT PRIMARY KEY, last_sync TIMESTAMPTZ NOT NULL)")
    c.commit()

def get_watermark(c,kind):
    row=c.execute("SELECT last_sync FROM sync_watermarks WHERE kind=%s",(kind,)).fetchone()
    return row[0] if row else None

def set_watermark(c,kind,ts):
    c.execute("INSERT INTO sync_watermarks (kind,last_sync) VALUES (%s,%s) ON CONFLICT (kind) DO UPDATE SET last_sync=EXCLUDED.last_sync",(kind,ts))

def build(raw,accounts_existing=None):
    accounts={}
    for r in raw["accounts"]:
        k=key(r.get("z_Kp_CRMaccounts_txt"))
        if not k or not s(r.get("Account_Name_stored")): continue
        accounts[k]=(k,s(r["Account_Name_stored"]),type_codes(r.get("Account_Type")),
            key(r.get("z_Kf_ParentAccount")) or None,key(r.get("z_Kf_RootParentAccount")) or None,
            num(r.get("Sales_YTD")),num(r.get("Sales_PreviousYr")),num(r.get("Quotes_YTD")),day(r.get("Last_Order")),
            s(r.get("Addr_Address")),s(r.get("Addr_City")),s(r.get("Addr_State")),s(r.get("Addr_Zip")),
            s(r.get("Homepage")),s(r.get("Category")))
    numeric_to_uuid={}
    for r in raw["accounts"]:
        uuid=key(r.get("z_Kp_CRMaccounts_txt"))
        if not uuid: continue
        for fk in ("z_Kf_Customer","z_Kf_Enduser","z_Kf_Engineering"):
            v=s(r.get(fk))
            if v and v.isdigit(): numeric_to_uuid[v]=uuid
    all_ids=set(accounts.keys()) | (accounts_existing or set())
    links={}; best={}
    for r in raw["links"]:
        c=s(r.get("_Kf_Buyer")).split(".")[0]; a=key(r.get("_Kf_CRMaccount"))
        if not c or not c.isdigit() or a not in all_ids: continue
        if (c,a) not in links: links[(c,a)]=(c,a,0.0,0.0,0.0)
        if c not in best: best[c]=(a,0)
    contacts={}
    for r in raw["contacts"]:
        c=s(r.get("__Kp_Buyer")).split(".")[0]
        name=(s(r.get("Name_First"))+" "+s(r.get("Name_Last"))).strip()
        if not c or not c.isdigit() or not name: continue
        cur=key(r.get("_Kf_CRMaccount_Current"))
        if cur not in all_ids: cur=best.get(c,(None,0))[0]
        contacts[c]=(c,name,cur,s(r.get("ContactTitle")),s(r.get("Email")),
            s(r.get("Direct")),s(r.get("Mobile")),s(r.get("Address_Street")),
            s(r.get("Address_City")),s(r.get("Address_State")),s(r.get("Address_Zip")),
            s(r.get("LinkedIn")),False,True,None,None)
    links={k:v for k,v in links.items() if k[0] in contacts}
    offices={}; unplaced=0
    for r in raw["offices"]:
        oid=s(r.get("__Kp_CRMaccountOffice"))
        if not oid: continue
        raw_fk=s(r.get("_Kf_CRMaccount"))
        a=key(raw_fk) or numeric_to_uuid.get(raw_fk,"")
        if not a or a not in all_ids: unplaced+=1; continue
        offices[oid]=(oid,a,s(r.get("OfficeType")),s(r.get("Addr_Address")),
            s(r.get("Addr_City")),s(r.get("Addr_State")),s(r.get("Addr_Zip")),s(r.get("Verified_Status")))
    return {"accounts":accounts,"contacts":contacts,"links":links,"offices":offices,"unplaced_offices":unplaced}

def apply_to_postgres(c,data,full_links):
    cur=c.cursor()
    cur.executemany("""INSERT INTO accounts (id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order,address,city,state,zip,homepage,category,updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
        ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,types=EXCLUDED.types,parent_id=EXCLUDED.parent_id,root_id=EXCLUDED.root_id,sales_ytd=EXCLUDED.sales_ytd,sales_py=EXCLUDED.sales_py,quotes_ytd=EXCLUDED.quotes_ytd,last_order=EXCLUDED.last_order,address=EXCLUDED.address,city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,homepage=EXCLUDED.homepage,category=EXCLUDED.category,updated_at=now()""",
        list(data["accounts"].values()))
    cur.executemany("""INSERT INTO contacts (id,name,account_id,title,email,phone_direct,phone_mobile,address,city,state,zip,linkedin,work_remote,active,last_quote,last_job,updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
        ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,account_id=EXCLUDED.account_id,title=EXCLUDED.title,email=EXCLUDED.email,phone_direct=EXCLUDED.phone_direct,phone_mobile=EXCLUDED.phone_mobile,address=EXCLUDED.address,city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,linkedin=EXCLUDED.linkedin,work_remote=EXCLUDED.work_remote,active=EXCLUDED.active,last_quote=EXCLUDED.last_quote,last_job=EXCLUDED.last_job,updated_at=now()""",
        list(data["contacts"].values()))
    if full_links: cur.execute("DELETE FROM contact_accounts")
    if data["links"]: cur.executemany("INSERT INTO contact_accounts (contact_id,account_id,sales_ytd,sales_py,quotes_ytd) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",list(data["links"].values()))
    if data["offices"]: cur.executemany("""INSERT INTO account_offices (id,account_id,office_type,address,city,state,zip,notes,source,updated_by,updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'"'"'fm'"'"','"'"'filemaker'"'"',now())
        ON CONFLICT (id) DO UPDATE SET account_id=EXCLUDED.account_id,office_type=EXCLUDED.office_type,address=EXCLUDED.address,city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,updated_at=now() WHERE account_offices.source='"'"'fm'"'"'""",
        [(o[0],o[1],o[2],o[3],o[4],o[5],o[6],("Verified: "+o[7]) if o[7] else "") for o in data["offices"].values()])

def probe():
    host,db,user,pw=_cfg(); token=_login(host,db,user,pw)
    try:
        for kind in LAYOUTS:
            rows=fetch_full(kind,token,host,db)[:3]
            print(f"\n== {LAYOUTS[kind]} ({kind})")
            for r in rows:
                show={k:v for k,v in r.items() if k.startswith("_") or k.startswith("z_")}
                show["_name"]=(r.get("Account_Name_stored") or f"{r.get(chr(78)+'ame_First','')} {r.get(chr(78)+'ame_Last','')}".strip() or r.get("OfficeType",""))
                print("  ",json.dumps(show,default=str))
    finally: _logout(host,db,token)

def sync(force_full=False):
    t0=time.time(); now=datetime.utcnow()
    host,db,user,pw=_cfg()
    with psycopg.connect(os.environ["DATABASE_URL"]) as c:
        ensure_watermarks(c)
        wm={kind:get_watermark(c,kind) for kind in LAYOUTS}
        is_first=all(v is None for v in wm.values())
        do_full=force_full or is_first
        mode="full" if do_full else "incremental"
        accounts_existing=set()
        if not do_full:
            accounts_existing={r[0] for r in c.execute("SELECT id FROM accounts").fetchall()}
        run_id=c.execute("INSERT INTO sync_runs (mode) VALUES (%s) RETURNING id",(mode,)).fetchone()[0]
        c.commit()
        before={t:c.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("accounts","contacts","contact_accounts")}
        before["fm_offices"]=c.execute("SELECT count(*) FROM account_offices WHERE source='"'"'fm'"'"'").fetchone()[0]
    token=_login(host,db,user,pw)
    try:
        raw={}; fetched={}
        for kind in LAYOUTS:
            if do_full or wm[kind] is None:
                raw[kind]=fetch_full(kind,token,host,db)
            else:
                raw[kind]=fetch_delta(kind,token,host,db,wm[kind])
            fetched[kind]=len(raw[kind])
            print(f"  {kind}: {fetched[kind]} ({'full' if do_full or wm[kind] is None else 'delta'})")
    finally: _logout(host,db,token)
    data=build(raw,accounts_existing if not do_full else None)
    summary={"mode":mode,"fetched":fetched,"usable":{k:len(data[k]) for k in ("accounts","contacts","links","offices")},"unplaced_offices":data["unplaced_offices"],"postgres_before":before}
    with psycopg.connect(os.environ["DATABASE_URL"]) as c:
        with c.transaction():
            apply_to_postgres(c,data,full_links=do_full)
            for kind in LAYOUTS: set_watermark(c,kind,now)
        after={t:c.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("accounts","contacts","contact_accounts")}
        summary["postgres_after"]=after; summary["seconds"]=round(time.time()-t0,1)
        c.execute("UPDATE sync_runs SET finished_at=now(),ok=true,summary=%s WHERE id=%s",(json.dumps(summary),run_id))
        c.commit()
    print(f"\n{mode.upper()} SYNC COMPLETE\n"+json.dumps(summary,indent=2))

if __name__=="__main__":
    cmd=sys.argv[1] if len(sys.argv)>1 else "run"
    if cmd=="probe": probe()
    elif cmd=="full": sync(force_full=True)
    elif cmd=="run": sync(force_full=False)
    else: print("Usage: probe | full | run"); sys.exit(1)
'''
open('app/fmsync.py','w',encoding='utf-8').write(content)
print('written', len(content), 'chars')
