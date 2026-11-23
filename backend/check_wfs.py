import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    r = c.execute("""
        SELECT a.id, a.name, a.root_id,
               COALESCE(SUM(CASE WHEN aq.record_type='quote'
                 AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now())
                 THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.name ILIKE '%williams field%'
        GROUP BY a.id, a.name, a.root_id
    """).fetchone()
    print("Williams Field Services:", dict(r))

    # Check its quotes directly
    rows = c.execute("""
        SELECT record_type, quote_date, job_date, total_amount
        FROM account_quotes
        WHERE account_id=%s
          AND record_type='quote'
          AND COALESCE(quote_date,job_date) >= '2026-01-01'
        LIMIT 5
    """, (r['id'],)).fetchall()
    print(f"\nDirect quotes ({len(rows)}):")
    for q in rows: print(" ", dict(q))
