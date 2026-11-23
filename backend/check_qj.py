import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Quote totals in account_quotes
    r = c.execute("SELECT COUNT(*) cnt, COUNT(account_id) with_acct FROM account_quotes").fetchone()
    print("account_quotes:", dict(r))

    # Check quotes_ytd on accounts
    r2 = c.execute("SELECT COUNT(*) cnt FROM accounts WHERE quotes_ytd > 0").fetchone()
    print("accounts with quotes_ytd > 0:", dict(r2))

    # Check contact_accounts table
    r3 = c.execute("SELECT COUNT(*) cnt, COUNT(NULLIF(sales_ytd,0)) with_sales FROM contact_accounts").fetchone()
    print("contact_accounts:", dict(r3))

    # Sample contact_accounts
    rows = c.execute("""
        SELECT ca.contact_id, ca.account_id, ca.sales_ytd, ca.sales_py, ca.quotes_ytd,
               c.name as contact, a.name as account
        FROM contact_accounts ca
        JOIN contacts c ON c.id = ca.contact_id
        JOIN accounts a ON a.id = ca.account_id
        WHERE ca.sales_ytd > 0
        LIMIT 5
    """).fetchall()
    print("\nContact sales samples:")
    for r in rows: print(" ", dict(r))
