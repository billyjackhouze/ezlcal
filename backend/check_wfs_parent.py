import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT name, parent_id, root_id,
               COALESCE(SUM(CASE WHEN aq.record_type='quote'
                 AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now())
                 THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE root_id='6AA6F04C-E9F4-4E98-BA8E-BEBE6F635D54'
        GROUP BY a.id, name, parent_id, root_id
        ORDER BY quotes_ytd DESC LIMIT 10
    """).fetchall()
    print("Williams family (parent_id vs root_id):")
    for r in rows:
        print(f"  {r['name']}")
        print(f"    parent_id={r['parent_id']}")
        print(f"    root_id={r['root_id']}")
        print(f"    quotes_ytd=${float(r['quotes_ytd']):,.0f}")
