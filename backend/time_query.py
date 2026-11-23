import psycopg, os, time
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    t0 = time.time()
    rows = c.execute("""
        SELECT a.id, a.name,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        GROUP BY a.id, a.name
        ORDER BY quotes_ytd DESC LIMIT 10
    """).fetchall()
    t1 = time.time()
    print(f"Query took {t1-t0:.2f}s")
    for r in rows:
        if float(r['quotes_ytd']) > 0:
            print(f"  {r['name']}: ${float(r['quotes_ytd']):,.0f}")
