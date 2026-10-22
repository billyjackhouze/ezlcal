import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    cur = c.cursor()
    cur.execute("DELETE FROM account_offices WHERE office_type = %s", ("Billing",))
    deleted = cur.rowcount
    print(f"Cleared {deleted} existing billing offices")

    cur.execute("""
        INSERT INTO account_offices (id, account_id, office_type, address, city, state, zip, deleted)
        SELECT
            gen_random_uuid()::text,
            account_id,
            'Billing',
            billing_address,
            billing_city,
            billing_state,
            billing_zip,
            false
        FROM (
            SELECT DISTINCT
                account_id,
                trim(billing_address) AS billing_address,
                trim(billing_city)    AS billing_city,
                trim(billing_state)   AS billing_state,
                trim(billing_zip)     AS billing_zip
            FROM account_quotes
            WHERE billing_address IS NOT NULL AND trim(billing_address) != ''
              AND billing_city    IS NOT NULL AND trim(billing_city)    != ''
              AND account_id IS NOT NULL
        ) uniq
    """)
    inserted = cur.rowcount
    c.commit()

    total = c.execute("SELECT count(*) FROM account_offices").fetchone()["count"]
    with_addr = c.execute(
        "SELECT count(*) FROM account_offices WHERE address IS NOT NULL AND address != '' AND NOT deleted"
    ).fetchone()["count"]
    print(f"Inserted: {inserted} unique billing addresses")
    print(f"Total offices: {total}")
    print(f"Visible (not deleted): {with_addr}")
    print()
    rows = c.execute(
        "SELECT a.name, count(*) as cnt FROM account_offices o"
        " JOIN accounts a ON a.id = o.account_id"
        " WHERE NOT o.deleted GROUP BY a.name ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    print("Accounts with most addresses:")
    for r in rows: print(f"  {r['name']}: {r['cnt']}")
