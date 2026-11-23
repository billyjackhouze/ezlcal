import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check how contact_accounts is populated - what is the source?
    rows = c.execute("""
        SELECT ca.sales_ytd, ca.sales_py, ca.quotes_ytd,
               c.name as contact, a.name as account
        FROM contact_accounts ca
        JOIN contacts c ON c.id=ca.contact_id
        JOIN accounts a ON a.id=ca.account_id
        LIMIT 5
    """).fetchall()
    print("Sample contact_accounts:")
    for r in rows: print(" ", dict(r))

    # Check staff table - does it have login names?
    rows2 = c.execute("SELECT id, name, dept FROM staff LIMIT 10").fetchall()
    print("\nStaff:")
    for r in rows2: print(" ", dict(r))
