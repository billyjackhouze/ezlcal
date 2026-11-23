import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

# Use same connection string as the app pool
db = os.environ["DATABASE_URL"]
print("DB:", db[:50])

with psycopg.connect(db, row_factory=psycopg.rows.dict_row) as c:
    # Run exact bootstrap query, check Williams
    rows = c.execute("""
        SELECT a.name,
               float8(COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0)) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.name IN ('THE WILLIAMS COMPANIES, INC.','WILLIAMS FIELD SERVICES','SUNLAND CONSTRUCTION')
        GROUP BY a.id, a.name
        ORDER BY quotes_ytd DESC
    """).fetchall()
    for r in rows:
        print(f"  {r['name']}: ${r['quotes_ytd']:,.0f}")
