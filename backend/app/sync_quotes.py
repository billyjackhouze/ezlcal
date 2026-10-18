"""Sync quotes and jobs from FileMaker API_SCHEDULE layout into Postgres.

  python -m app.sync_quotes          sync last 3 years
  python -m app.sync_quotes --full   sync all records

Uses API_SCHEDULE layout (minimal fields, fast pagination).
Quotes: QUOTE='QUOTE', Jobs: Watch JOB='JOB'.
Links to accounts via _Kf_Customer -> CRM_accounts.z_Kf_Customer.
"""
import json, os, sys, time, ssl, urllib.request, urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DB = os.environ["DATABASE_URL"]
PAGE = 1000
CUTOFF_YEARS = 3


def _cfg():
    host = os.environ.get("FM_HOST", "fms26.alamark.com").strip().rstrip("/")
    if not host.startswith("http"):
        host = "https://" + host
    return host, "ez-line", os.environ["FM_USER"], os.environ["FM_PASSWORD"]


def _login(host, db, user, pw):
    import base64
    url = f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions"
    b64 = base64.b64encode(f"{user}:{pw}".encode()).decode()
    req = urllib.request.Request(url, method="POST", data=b"{}",
          headers={"Authorization": f"Basic {b64}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
        return json.loads(r.read())["response"]["token"]


def _logout(host, db, token):
    url = f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions/{token}"
    try:
        urllib.request.urlopen(urllib.request.Request(url, method="DELETE",
            headers={"Authorization": f"Bearer {token}"}), timeout=10,
            context=ssl.create_default_context())
    except Exception:
        pass


def _get_page(host, db, token, layout, offset):
    url = (f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}"
           f"/layouts/{urllib.parse.quote(layout)}/records"
           f"?_offset={offset}&_limit={PAGE}")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120,
                                        context=ssl.create_default_context()) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == 2:
                raise SystemExit(f"FM error: {e}")
            time.sleep(2 * (attempt + 1))
    return {}


def s(v):
    return "" if v is None else str(v).strip().replace(chr(0), "")


def parse_date(v):
    v = s(v)
    if not v:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def num(v):
    try:
        return float(str(v).replace(",", "") or 0)
    except (TypeError, ValueError):
        return 0.0


def ensure_schema(c):
    c.execute("""
        CREATE TABLE IF NOT EXISTS account_quotes (
            id              TEXT PRIMARY KEY,
            account_id      TEXT REFERENCES accounts(id) ON DELETE CASCADE,
            fm_customer_id  TEXT,
            job_number      TEXT,
            record_type     TEXT,
            quote_date      DATE,
            job_date        DATE,
            sales_person    TEXT,
            buyer_name      TEXT,
            customer_name   TEXT,
            project         TEXT,
            total_amount    NUMERIC(14,2),
            updated_at      TIMESTAMPTZ DEFAULT now()
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS aq_account_id ON account_quotes (account_id)")
    c.execute("CREATE INDEX IF NOT EXISTS aq_dates ON account_quotes (quote_date, job_date)")
    c.commit()


def build_cust_map(host, db, token):
    cust_map = {}
    offset = 1
    print("Building customer ID map...")
    while True:
        data = _get_page(host, db, token, "API_CRM_Accounts", offset)
        records = data.get("response", {}).get("data", [])
        for rec in records:
            fd = rec.get("fieldData", {})
            uuid = s(fd.get("z_Kp_CRMaccounts_txt"))
            cust_id = s(fd.get("z_Kf_Customer"))
            if uuid and cust_id and cust_id.isdigit():
                cust_map[cust_id] = uuid
        if len(records) < PAGE:
            break
        offset += PAGE
    print(f"  {len(cust_map)} customer mappings")
    return cust_map


def fetch_schedule(host, db, token, full=False):
    """Fetch from API_SCHEDULE — minimal layout, fast pagination with client-side date filter."""
    cutoff = datetime.now().date() - timedelta(days=365 * CUTOFF_YEARS)
    rows, offset, scanned = [], 1, 0
    print(f"Fetching API_SCHEDULE ({'all' if full else f'last {CUTOFF_YEARS} years'})...")
    while True:
        data = _get_page(host, db, token, "API_SCHEDULE", offset)
        records = data.get("response", {}).get("data", [])
        scanned += len(records)
        for rec in records:
            fd = rec.get("fieldData", {})
            if not full:
                qd = parse_date(fd.get("QUOTE_DATE"))
                jd = parse_date(fd.get("JOB_DATE") or fd.get("DATE SHIPPED"))
                best = jd or qd
                if best and best < cutoff:
                    continue
            rows.append(fd)
        if len(records) < PAGE:
            break
        offset += PAGE
        print(f"  scanned {scanned}, kept {len(rows)}...")
    print(f"  {scanned} total scanned, {len(rows)} in date range")
    return rows


def run(full=False):
    host, db, user, pw = _cfg()

    with psycopg.connect(DB, row_factory=dict_row) as c:
        ensure_schema(c)

    token = _login(host, db, user, pw)
    try:
        cust_map = build_cust_map(host, db, token)
        schedule_rows = fetch_schedule(host, db, token, full)
    finally:
        _logout(host, db, token)

    cutoff = datetime.now().date() - timedelta(days=365 * CUTOFF_YEARS)
    upsert_rows = []
    skip = 0

    for r in schedule_rows:
        job_num = s(r.get("JOB_NUMBER"))
        if not job_num:
            skip += 1
            continue
        fm_cust_id = s(r.get("_Kf_Customer"))
        account_id = cust_map.get(fm_cust_id)
        if not account_id:
            skip += 1
            continue

        quote_date = parse_date(r.get("QUOTE_DATE"))
        job_date = parse_date(r.get("JOB_DATE") or r.get("DATE SHIPPED"))
        record_type = "quote" if s(r.get("QUOTE")) == "QUOTE" else "job"
        row_id = f"{job_num}_{fm_cust_id}_{record_type}"

        upsert_rows.append((
            row_id, account_id, fm_cust_id, job_num, record_type,
            quote_date, job_date,
            s(r.get("SALES PERSON")), s(r.get("Buyer Name")),
            s(r.get("CUSTOMER NAME")), s(r.get("REFERENCE_project")),
            num(r.get("TOTAL JOB AMOUNT calc", 0)),
        ))

    print(f"Upserting {len(upsert_rows)} rows ({skip} skipped)...")

    with psycopg.connect(DB, row_factory=dict_row) as c:
        with c.transaction():
            c.executemany("""
                INSERT INTO account_quotes
                    (id, account_id, fm_customer_id, job_number, record_type,
                     quote_date, job_date, sales_person, buyer_name,
                     customer_name, project, total_amount, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
                ON CONFLICT (id) DO UPDATE SET
                    account_id=EXCLUDED.account_id,
                    quote_date=EXCLUDED.quote_date, job_date=EXCLUDED.job_date,
                    sales_person=EXCLUDED.sales_person, buyer_name=EXCLUDED.buyer_name,
                    customer_name=EXCLUDED.customer_name, project=EXCLUDED.project,
                    total_amount=EXCLUDED.total_amount, updated_at=now()
            """, upsert_rows)
        counts = c.execute("""
            SELECT record_type, count(*) n FROM account_quotes GROUP BY record_type
        """).fetchall()
        for row in counts:
            print(f"  {row['record_type']}: {row['n']} in DB")

    print(f"Done: {len(upsert_rows)} upserted, {skip} skipped.")


if __name__ == "__main__":
    run(full="--full" in sys.argv)
