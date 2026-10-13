"""Pull accounts, contacts, contact<->account links and offices from FileMaker (OData) into Postgres.

READ-ONLY on FileMaker: this module only ever sends GET requests.

  python -m app.fmsync credentials   store FM_USER / FM_PASSWORD in backend\\.env (prompted, not echoed)
  python -m app.fmsync probe         fetch 3 rows per table and print the raw key values (no writes anywhere)
  python -m app.fmsync dry-run       fetch everything, print what would change, write nothing
  python -m app.fmsync run           fetch everything and apply it to Postgres in one transaction

Fields deliberately NOT synced: Buyer home address, photos, duplicate-review fields.
"""
import base64
import getpass
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
load_dotenv(ENV)

UUID_RE = re.compile(r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PAGE = 1000

TABLES = {
    "accounts": ("CRM_ACCOUNTS", [
        "z_Kp_CRMaccounts_txt", "Account_Name_stored", "Account_Type", "Category", "z_Kf_ParentAccount",
        "z_Kf_RootParentAccount", "Sales_YTD", "Sales_PreviousYr", "Quotes_YTD", "Last_Order",
        "Addr_Address", "Addr_City", "Addr_State", "Addr_Zip", "Homepage"]),
    "contacts": ("BUYER", [
        "__Kp_Buyer", "Name_First", "Name_Last", "ContactTitle", "ContactType", "Email", "Direct", "Mobile",
        "Address_Street", "Address_City", "Address_State", "Address_Zip", "LinkedIn", "WorkRemote", "Active",
        "Last_Quote", "Last_Job", "_Kf_CRMaccount_Current"]),
    "links": ("CRM_BuyerAccount", [
        "__Kp_CRMBuyerAccount", "_Kf_Buyer", "z_Kp_CRMaccounts_txt", "_Kf_CRMaccountOffice",
        "Sales_YearToDate", "Sales_PreviousYear", "Quotes_YearToDate"]),
    "offices": ("CRM_AccountOffice", [
        "__Kp_CRMaccountOffice", "_Kf_CRMaccount", "OfficeType", "Addr_Address", "Addr_City", "Addr_State",
        "Addr_Zip", "Verified_Status"]),
}
TYPE_CODES = {"customer": "C", "enduser": "U", "end user": "U", "engref": "G", "engineering": "G",
              "engineering company": "G"}


# ---------- FileMaker OData (GET only) ----------
def _cfg():
    host = os.environ.get("FM_HOST", "https://fms26.alamark.com").rstrip("/")
    db = os.environ.get("FM_DB", "ez-line")
    user, pw = os.environ.get("FM_USER"), os.environ.get("FM_PASSWORD")
    if not user or not pw:
        sys.exit("FM_USER / FM_PASSWORD are not set. Run: python -m app.fmsync credentials")
    return host, db, user, pw


def _get(url: str, auth: str) -> dict:
    req = urllib.request.Request(url, method="GET", headers={"Authorization": "Basic " + auth, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120, context=ssl.create_default_context()) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:400]
            if e.code in (401, 403):
                sys.exit(f"FileMaker refused the login ({e.code}). Check the account has the fmodata privilege. {body}")
            if attempt == 2:
                raise SystemExit(f"OData error {e.code} for {url}\n{body}")
        except urllib.error.URLError as e:
            if attempt == 2:
                raise SystemExit(f"Could not reach FileMaker OData: {e.reason}")
        time.sleep(2 * (attempt + 1))
    return {}


def _q(field: str) -> str:
    return field if IDENT_RE.match(field) else '"' + field + '"'


def fetch(kind: str, limit: int | None = None) -> list[dict]:
    host, db, user, pw = _cfg()
    to, fields = TABLES[kind]
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
    base = f"{host}/fmi/odata/v4/{urllib.parse.quote(db)}/{urllib.parse.quote(to)}"
    rows, skip = [], 0
    while True:
        top = min(PAGE, limit - len(rows)) if limit else PAGE
        qs = urllib.parse.urlencode({"$select": ",".join(_q(f) for f in fields), "$top": top, "$skip": skip}, safe="$,\"")
        page = _get(f"{base}?{qs}", auth).get("value", [])
        rows.extend(page)
        if len(page) < top or (limit and len(rows) >= limit):
            return rows
        skip += top


# ---------- normalising ----------
def s(v) -> str:
    return "" if v is None else str(v).strip()


def num(v) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def day(v):
    v = s(v)[:10]
    return v if re.match(r"^\d{4}-\d{2}-\d{2}$", v) else None


def key(v) -> str:
    """Account keys are UUID text. Returns '' when FileMaker handed back something else (e.g. a mangled number)."""
    v = s(v).upper()
    return v if UUID_RE.match(v) else ""


def type_codes(v) -> str:
    out = {TYPE_CODES.get(t.strip().lower(), "") for t in re.split(r"[\r\n]+", s(v)) if t.strip()}
    return "".join(sorted(c for c in out if c))


def build(raw: dict) -> dict:
    accounts = {}
    for r in raw["accounts"]:
        k = key(r.get("z_Kp_CRMaccounts_txt"))
        if not k or not s(r.get("Account_Name_stored")):
            continue
        accounts[k] = (k, s(r["Account_Name_stored"]), type_codes(r.get("Account_Type")),
                       key(r.get("z_Kf_ParentAccount")) or None, key(r.get("z_Kf_RootParentAccount")) or None,
                       num(r.get("Sales_YTD")), num(r.get("Sales_PreviousYr")), num(r.get("Quotes_YTD")),
                       day(r.get("Last_Order")), s(r.get("Addr_Address")), s(r.get("Addr_City")),
                       s(r.get("Addr_State")), s(r.get("Addr_Zip")), s(r.get("Homepage")), s(r.get("Category")))

    links, best = {}, {}
    for r in raw["links"]:
        c, a = s(r.get("_Kf_Buyer")).split(".")[0], key(r.get("z_Kp_CRMaccounts_txt"))
        if not c or a not in accounts:
            continue
        row = (c, a, num(r.get("Sales_YearToDate")), num(r.get("Sales_PreviousYear")), num(r.get("Quotes_YearToDate")))
        prev = links.get((c, a))
        if not prev or row[2] + row[3] > prev[2] + prev[3]:
            links[(c, a)] = row
        score = row[2] + row[3] + row[4]
        if c not in best or score > best[c][1]:
            best[c] = (a, score)

    contacts, bad_current = {}, 0
    for r in raw["contacts"]:
        c = s(r.get("__Kp_Buyer")).split(".")[0]
        name = (s(r.get("Name_First")) + " " + s(r.get("Name_Last"))).strip()
        if not c or not name:
            continue
        cur = key(r.get("_Kf_CRMaccount_Current"))
        if s(r.get("_Kf_CRMaccount_Current")) and not cur:
            bad_current += 1
        if cur not in accounts:
            cur = best.get(c, (None, 0))[0]
        active = s(r.get("Active")).lower() not in ("inactive", "no", "n", "0", "false")
        contacts[c] = (c, name, cur, s(r.get("ContactTitle")), s(r.get("Email")), s(r.get("Direct")), s(r.get("Mobile")),
                       s(r.get("Address_Street")), s(r.get("Address_City")), s(r.get("Address_State")),
                       s(r.get("Address_Zip")), s(r.get("LinkedIn")), num(r.get("WorkRemote")) > 0, active,
                       day(r.get("Last_Quote")), day(r.get("Last_Job")))
    links = {k: v for k, v in links.items() if k[0] in contacts}

    office_acct_via_links = {}
    for r in raw["links"]:
        o, a = s(r.get("_Kf_CRMaccountOffice")), key(r.get("z_Kp_CRMaccounts_txt"))
        if o and a:
            office_acct_via_links[o] = a
    offices, unplaced = {}, []
    for r in raw["offices"]:
        oid = s(r.get("__Kp_CRMaccountOffice"))
        a = key(r.get("_Kf_CRMaccount")) or office_acct_via_links.get(oid, "")
        if not oid:
            continue
        if a not in accounts:
            unplaced.append(oid)
            continue
        offices[oid] = (oid, a, s(r.get("OfficeType")), s(r.get("Addr_Address")), s(r.get("Addr_City")),
                        s(r.get("Addr_State")), s(r.get("Addr_Zip")), s(r.get("Verified_Status")))
    return {"accounts": accounts, "contacts": contacts, "links": links, "offices": offices,
            "unplaced_offices": unplaced, "contacts_with_unreadable_current_key": bad_current}


# ---------- commands ----------
def credentials():
    user = input("FileMaker account for OData (e.g. ezlcal_sync): ").strip()
    pw = getpass.getpass("Password (not shown): ")
    lines = [l for l in ENV.read_text(encoding="utf-8").splitlines() if not l.startswith(("FM_USER=", "FM_PASSWORD="))]
    lines += [f"FM_USER={user}", f"FM_PASSWORD={pw}"]
    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Saved to backend\\.env. Next: python -m app.fmsync probe")


def probe():
    for kind in TABLES:
        rows = fetch(kind, limit=3)
        print(f"\n== {TABLES[kind][0]} ({kind}) -- {len(rows)} sample rows")
        for r in rows:
            show = {k: r.get(k) for k in TABLES[kind][1] if "K" in k or k.startswith("_")}
            show["_name"] = r.get("Account_Name_stored") or (s(r.get("Name_First")) + " " + s(r.get("Name_Last"))).strip() or r.get("OfficeType")
            print("   ", json.dumps(show, default=str))
    print("\nKeys should look like UUIDs (8-4-4-4-12) for accounts and whole numbers for contacts.")


def sync(apply: bool):
    t0 = time.time()
    raw = {k: fetch(k) for k in TABLES}
    data = build(raw)
    summary = {"fetched": {k: len(v) for k, v in raw.items()},
               "usable": {k: len(data[k]) for k in ("accounts", "contacts", "links", "offices")},
               "unplaced_offices": len(data["unplaced_offices"]),
               "contacts_with_unreadable_current_key": data["contacts_with_unreadable_current_key"]}
    with psycopg.connect(os.environ["DATABASE_URL"]) as c:
        run_id = c.execute("INSERT INTO sync_runs (mode) VALUES (%s) RETURNING id", ("run" if apply else "dry-run",)).fetchone()[0]
        c.commit()
        before = {t: c.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("accounts", "contacts", "contact_accounts")}
        before["fm_offices"] = c.execute("SELECT count(*) FROM account_offices WHERE source='fm'").fetchone()[0]
        summary["postgres_before"] = before
        try:
            with c.transaction(), c.cursor() as cur:
                cur.executemany(
                    """INSERT INTO accounts (id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order,
                                             address,city,state,zip,homepage,category,updated_at)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
                       ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,types=EXCLUDED.types,parent_id=EXCLUDED.parent_id,
                         root_id=EXCLUDED.root_id,sales_ytd=EXCLUDED.sales_ytd,sales_py=EXCLUDED.sales_py,
                         quotes_ytd=EXCLUDED.quotes_ytd,last_order=EXCLUDED.last_order,address=EXCLUDED.address,
                         city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,homepage=EXCLUDED.homepage,
                         category=EXCLUDED.category,updated_at=now()""", list(data["accounts"].values()))
                cur.executemany(
                    """INSERT INTO contacts (id,name,account_id,title,email,phone_direct,phone_mobile,address,city,state,zip,
                                             linkedin,work_remote,active,last_quote,last_job,updated_at)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
                       ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,account_id=EXCLUDED.account_id,title=EXCLUDED.title,
                         email=EXCLUDED.email,phone_direct=EXCLUDED.phone_direct,phone_mobile=EXCLUDED.phone_mobile,
                         address=EXCLUDED.address,city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,
                         linkedin=EXCLUDED.linkedin,work_remote=EXCLUDED.work_remote,active=EXCLUDED.active,
                         last_quote=EXCLUDED.last_quote,last_job=EXCLUDED.last_job,updated_at=now()""",
                    list(data["contacts"].values()))
                cur.execute("DELETE FROM contact_accounts")
                cur.executemany("INSERT INTO contact_accounts (contact_id,account_id,sales_ytd,sales_py,quotes_ytd) VALUES (%s,%s,%s,%s,%s)",
                                list(data["links"].values()))
                cur.executemany(
                    """INSERT INTO account_offices (id,account_id,office_type,address,city,state,zip,notes,source,updated_by,updated_at)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'fm','filemaker',now())
                       ON CONFLICT (id) DO UPDATE SET account_id=EXCLUDED.account_id,office_type=EXCLUDED.office_type,
                         address=EXCLUDED.address,city=EXCLUDED.city,state=EXCLUDED.state,zip=EXCLUDED.zip,
                         updated_at=now() WHERE account_offices.source='fm'""",
                    [(o[0], o[1], o[2], o[3], o[4], o[5], o[6], ("Verified: " + o[7]) if o[7] else "") for o in data["offices"].values()])
                if not apply:
                    raise _DryRun()
        except _DryRun:
            pass
        after = {t: c.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("accounts", "contacts", "contact_accounts")}
        summary["postgres_after"] = after
        summary["seconds"] = round(time.time() - t0, 1)
        c.execute("UPDATE sync_runs SET finished_at=now(), ok=true, summary=%s WHERE id=%s", (json.dumps(summary), run_id))
        c.commit()
    label = "APPLIED" if apply else "DRY RUN (nothing written)"
    print(f"\n{label}\n" + json.dumps(summary, indent=2))
    if not apply:
        print("\nLooks right? Run: python -m app.fmsync run")


class _DryRun(Exception):
    pass


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"credentials": credentials, "probe": probe, "dry-run": lambda: sync(False), "run": lambda: sync(True)}.get(
        cmd, lambda: (print(__doc__), sys.exit(1)))()
