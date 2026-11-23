import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Get White Water family quotes direct from new query logic
    rows = c.execute("""
        SELECT a.name, a.id,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' 
                 AND COALESCE(aq.quote_date,aq.job_date) >= '2026-01-01'
                 AND COALESCE(aq.quote_date,aq.job_date) < '2027-01-01'
                 THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.name ILIKE '%white water%'
           OR a.root_id='01994BF8-B3F9-2B4B-96FB-85439B6B9736'
        GROUP BY a.id, a.name
        ORDER BY quotes_ytd DESC
    """).fetchall()
    for r in rows:
        print(f"{r['name']}: quotes_ytd=${float(r['quotes_ytd']):,.0f}")

    # Also check main.py to confirm fix is in place
    src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text()
    print("\nquote fix in main.py:", "COALESCE(aq.quote_date,aq.job_date)" in src)
