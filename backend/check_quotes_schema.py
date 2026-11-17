import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Postgres account_quotes columns
    cols = c.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name='account_quotes' 
        ORDER BY ordinal_position
    """).fetchall()
    print("=== account_quotes columns ===")
    for r in cols: print(f"  {r['column_name']}: {r['data_type']}")
    
    # Row counts
    total = c.execute("SELECT COUNT(*) n FROM account_quotes").fetchone()["n"]
    jobs = c.execute("SELECT COUNT(*) n FROM account_quotes WHERE is_job=true").fetchone()["n"]
    quotes = c.execute("SELECT COUNT(*) n FROM account_quotes WHERE is_job=false").fetchone()["n"]
    print(f"\nTotal: {total}, Jobs: {jobs}, Quotes: {quotes}")
    
    # Sample row
    sample = c.execute("SELECT * FROM account_quotes LIMIT 1").fetchone()
    print("\nSample row keys:", list(sample.keys()) if sample else "empty")
