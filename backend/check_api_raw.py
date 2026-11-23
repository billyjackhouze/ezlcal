import psycopg, os, json
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Run exact query from main.py
    rows = c.execute("""
        SELECT a.id, a.name, a.types, a.parent_id, a.root_id,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS sales_ytd,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now())-1 THEN aq.total_amount ELSE 0 END),0) AS sales_py,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd,
               a.last_order, a.address, a.city, a.state, a.zip, a.homepage
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        WHERE a.name ILIKE '%williams field%'
        GROUP BY a.id, a.name, a.types, a.parent_id, a.root_id, a.last_order, a.address, a.city, a.state, a.zip, a.homepage
    """).fetchone()
    # Show as array (what the API sends)
    arr = [rows['id'], rows['name'], rows['types'], rows['parent_id'], rows['root_id'],
           float(rows['sales_ytd']), float(rows['sales_py']), float(rows['quotes_ytd']),
           str(rows['last_order']), rows['address'], rows['city'], rows['state'], rows['zip'], rows['homepage']]
    print("Raw array (indices 0-13):")
    for i, v in enumerate(arr):
        print(f"  [{i}] {v}")
