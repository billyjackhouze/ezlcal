import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Find jobs with rich detail data
    rows = c.execute("""
        SELECT job_number, buyer_name, customer_name, po_number, 
               invoice_number, billing_terms, job_status,
               clamps_total, pipejacks_total, specialty_total
        FROM account_quotes
        WHERE record_type='job'
          AND (po_number!='' OR invoice_number!='' OR clamps_total>0)
        ORDER BY job_date DESC LIMIT 5
    """).fetchall()
    for r in rows: print(dict(r))
