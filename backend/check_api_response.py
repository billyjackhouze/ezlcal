import urllib.request, json, ssl, base64, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

# Hit the local API directly to see what it returns
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login first
db_url = os.environ["DATABASE_URL"]
import psycopg
with psycopg.connect(db_url, row_factory=psycopg.rows.dict_row) as c:
    # Get Williams directly from the new query
    r = c.execute("""
        SELECT a.name,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS sales_ytd,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now())-1 THEN aq.total_amount ELSE 0 END),0) AS sales_py,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.name ILIKE '%williams companies%'
        GROUP BY a.id, a.name
    """).fetchone()
    print("Williams from API query:", dict(r))

    # Check a child with quotes
    r2 = c.execute("""
        SELECT a.name, a.root_id,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.root_id='6AA6F04C-E9F4-4E98-BA8E-BEBE6F635D54'
        GROUP BY a.id, a.name, a.root_id
        HAVING SUM(CASE WHEN aq.record_type='quote' THEN aq.total_amount ELSE 0 END) > 0
        ORDER BY quotes_ytd DESC LIMIT 5
    """).fetchall()
    print("\nWilliams children with quotes:")
    for r in r2: print(f"  {r['name']}: ${float(r['quotes_ytd']):,.0f}")
