import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    c.execute("""
        UPDATE contact_accounts ca
        SET sales_ytd=sub.sales_ytd, sales_py=sub.sales_py, quotes_ytd=sub.quotes_ytd
        FROM (
            SELECT c.id as contact_id, ca2.account_id,
                COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) as sales_ytd,
                COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now())-1 THEN aq.total_amount ELSE 0 END),0) as sales_py,
                COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) as quotes_ytd
            FROM contacts c
            JOIN contact_accounts ca2 ON ca2.contact_id=c.id
            JOIN account_quotes aq ON aq.account_id=ca2.account_id
                AND LOWER(TRIM(aq.buyer_name))=LOWER(TRIM(c.name))
            GROUP BY c.id, ca2.account_id
        ) sub
        WHERE ca.contact_id=sub.contact_id AND ca.account_id=sub.account_id
    """)
    print("Contact sales updated")

import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    c.execute("""
        UPDATE accounts a SET last_order=sub.last_order
        FROM (
            SELECT account_id, MAX(COALESCE(job_date,quote_date)) as last_order
            FROM account_quotes WHERE record_type='job'
            GROUP BY account_id
        ) sub
        WHERE a.id=sub.account_id
          AND (a.last_order IS NULL OR a.last_order < sub.last_order)
    """)
    print("last_order updated")
