import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Replace Company offices with last job billing address per account
    cur = c.cursor()
    cur.execute("DELETE FROM account_offices WHERE office_type = 'Company' AND source = 'fm'")
    d = cur.rowcount
    cur.execute("""
        INSERT INTO account_offices
            (id, account_id, office_type, address, city, state, zip, notes, deleted, source, updated_at)
        SELECT DISTINCT ON (account_id)
            gen_random_uuid()::text,
            account_id,
            'Company',
            trim(billing_address),
            trim(billing_city),
            trim(billing_state),
            trim(billing_zip),
            trim(coalesce(buyer_name, '')),
            false,
            'fm',
            now()
        FROM account_quotes
        WHERE trim(coalesce(billing_address,'')) != ''
          AND trim(coalesce(billing_city,'')) != ''
          AND account_id IS NOT NULL
        ORDER BY account_id, coalesce(job_date, quote_date) DESC NULLS LAST
    """)
    i = cur.rowcount
    c.commit()
    print(f"Cleared {d}, inserted {i} company addresses")
    # Spot-check Bay Runner
    r = cur.execute("""
        SELECT o.address, o.city, o.state, o.notes, a.name
        FROM account_offices o JOIN accounts a ON a.id = o.account_id
        WHERE o.office_type = 'Company' AND o.source = 'fm'
          AND upper(a.name) LIKE '%BAY RUNNER%'
    """).fetchall()
    for row in r: print(f"  {row['name']}: {row['address']}, {row['city']} ({row['notes']})")
