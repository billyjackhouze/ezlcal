import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # account_quotes columns
    cols = c.execute("""
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_name='account_quotes' ORDER BY ordinal_position
    """).fetchall()
    print("account_quotes columns:")
    for r in cols: print(f"  {r['column_name']}: {r['data_type']}")

    # Sample rows
    rows = c.execute("""
        SELECT * FROM account_quotes LIMIT 3
    """).fetchall()
    print("\nSample rows:")
    for r in rows: print(" ", dict(r))
