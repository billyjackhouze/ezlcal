import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    result = c.execute("""
        UPDATE accounts a
        SET last_order = sub.last_order
        FROM (
            SELECT account_id,
                   MAX(COALESCE(job_date, quote_date)) as last_order
            FROM account_quotes
            WHERE record_type = 'job'
            GROUP BY account_id
        ) sub
        WHERE a.id = sub.account_id
          AND (a.last_order IS NULL OR a.last_order < sub.last_order)
        RETURNING a.id
    """)
    updated = len(result.fetchall())
    print(f"Updated last_order for {updated} accounts")
