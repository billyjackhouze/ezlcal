import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    # Update last_order including family (children) jobs
    result = c.execute("""
        UPDATE accounts a
        SET last_order = sub.last_order
        FROM (
            SELECT COALESCE(acc.root_id, acc.id) as root_id,
                   MAX(COALESCE(aq.job_date, aq.quote_date)) as last_order
            FROM account_quotes aq
            JOIN accounts acc ON acc.id = aq.account_id
            WHERE aq.record_type = 'job'
            GROUP BY COALESCE(acc.root_id, acc.id)
        ) sub
        WHERE (a.root_id = sub.root_id OR a.id = sub.root_id)
          AND (a.last_order IS NULL OR a.last_order < sub.last_order)
        RETURNING a.id
    """)
    updated = len(result.fetchall())
    print(f"Updated last_order for {updated} accounts")
    
    # Bump ETag
    c.execute("UPDATE account_offices SET updated_at=now() WHERE id=(SELECT id FROM account_offices LIMIT 1)")
    print("ETag bumped")
