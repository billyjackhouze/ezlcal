import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT p.name as parent, p.id,
               COUNT(DISTINCT c.id) as child_count,
               SUM(CASE WHEN aq.record_type='quote'
                 AND COALESCE(aq.quote_date,aq.job_date) >= '2026-01-01'
                 THEN aq.total_amount ELSE 0 END) AS family_quotes_ytd
        FROM accounts p
        JOIN accounts c ON c.root_id = p.id AND c.id != p.id
        JOIN account_quotes aq ON aq.account_id = c.id
        WHERE aq.record_type = 'quote'
          AND COALESCE(aq.quote_date, aq.job_date) >= '2026-01-01'
        GROUP BY p.id, p.name
        ORDER BY family_quotes_ytd DESC
        LIMIT 10
    """).fetchall()
    print("Parents with 2026 child quotes:")
    for r in rows:
        print(f"  {r['parent']}: {r['child_count']} children, family quotes=${float(r['family_quotes_ytd']):,.0f}")
