import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check all tables that might have line items
    tables = c.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public' ORDER BY table_name
    """).fetchall()
    print("Tables:", [r['table_name'] for r in tables])
    
    # Check account_quotes columns
    cols = c.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='account_quotes' ORDER BY ordinal_position
    """).fetchall()
    print("\naccount_quotes cols:", [r['column_name'] for r in cols])
