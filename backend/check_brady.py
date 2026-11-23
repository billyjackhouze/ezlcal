import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT ca.sales_ytd, ca.sales_py, ca.quotes_ytd,
               c.name, a.name as account
        FROM contact_accounts ca
        JOIN contacts c ON c.id=ca.contact_id
        JOIN accounts a ON a.id=ca.account_id
        WHERE c.name ILIKE '%brady%cluiss%' OR c.name ILIKE '%brady%clui%'
    """).fetchall()
    for r in rows: print(dict(r))
