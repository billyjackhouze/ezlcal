import psycopg, os, sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
DB = os.environ["DATABASE_URL"]

def run(dry_run=False):
    with psycopg.connect(DB, row_factory=psycopg.rows.dict_row) as conn:
        cur = conn.cursor()
        cur.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS contact_id TEXT")

        # Pass 1: one Company address per account (most recent job)
        cur.execute("DELETE FROM account_offices WHERE office_type = %s AND source = %s", ("Company","fm"))
        d1 = cur.rowcount
        cur.execute("""
            INSERT INTO account_offices
                (id, account_id, office_type, address, city, state, zip, notes, deleted, source, updated_at)
            SELECT DISTINCT ON (account_id)
                gen_random_uuid()::text, account_id, 'Company',
                trim(billing_address), trim(billing_city), trim(billing_state), trim(billing_zip),
                'Last job: ' || coalesce(job_number::text,''),
                false, 'fm', now()
            FROM account_quotes
            WHERE trim(coalesce(billing_address,'')) != ''
              AND trim(coalesce(billing_city,'')) != ''
              AND account_id IS NOT NULL
            ORDER BY account_id, coalesce(job_date, quote_date) DESC NULLS LAST
        """)
        i1 = cur.rowcount

        # Pass 2: one Buyer address per buyer per account (most recent job)
        cur.execute("DELETE FROM account_offices WHERE office_type = %s AND source = %s", ("Buyer","fm"))
        d2 = cur.rowcount
        cur.execute("""
            INSERT INTO account_offices
                (id, account_id, contact_id, office_type, address, city, state, zip, notes, deleted, source, updated_at)
            SELECT DISTINCT ON (q.account_id, upper(trim(q.buyer_name)))
                gen_random_uuid()::text, q.account_id, ct.id, 'Buyer',
                trim(q.billing_address), trim(q.billing_city), trim(q.billing_state), trim(q.billing_zip),
                trim(q.buyer_name),
                false, 'fm', now()
            FROM account_quotes q
            LEFT JOIN contacts ct ON upper(trim(ct.name)) = upper(trim(q.buyer_name))
            WHERE trim(coalesce(q.billing_address,'')) != ''
              AND trim(coalesce(q.billing_city,'')) != ''
              AND trim(coalesce(q.buyer_name,'')) != ''
              AND q.account_id IS NOT NULL
            ORDER BY q.account_id, upper(trim(q.buyer_name)),
                     coalesce(q.job_date, q.quote_date) DESC NULLS LAST
        """)
        i2 = cur.rowcount

        if dry_run:
            conn.rollback()
            print(f"DRY RUN: {i1} company, {i2} buyer addresses")
            return

        conn.commit()
        print(f"Company:  cleared {d1}, inserted {i1}")
        print(f"Buyer:    cleared {d2}, inserted {i2}")
        rows = cur.execute("""
            SELECT office_type, count(*) n FROM account_offices
            WHERE NOT deleted AND source='fm' GROUP BY office_type
        """).fetchall()
        for r in rows: print(f"  {r['office_type']}: {r['n']}")

if __name__ == "__main__":
    run(dry_run="--dry" in sys.argv)
