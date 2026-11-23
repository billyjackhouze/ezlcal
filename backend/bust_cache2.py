import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    # Check if updated_at exists on accounts
    r = c.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='accounts' AND column_name='updated_at'
    """).fetchone()
    print("accounts.updated_at exists:", r is not None)
    
    # Check contact_accounts count - that is also in the etag
    r2 = c.execute("SELECT COUNT(*) FROM contact_accounts").fetchone()
    print("contact_accounts count:", r2[0])
    
    # Bust by inserting and deleting a dummy contact_account
    # Actually just touch account_offices which is in the etag
    r3 = c.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='account_offices' AND column_name='updated_at'
    """).fetchone()
    print("account_offices.updated_at exists:", r3 is not None)
    
    if r3:
        c.execute("UPDATE account_offices SET updated_at=now() WHERE id=(SELECT id FROM account_offices LIMIT 1)")
        print("Busted via account_offices")
