import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT conname, pg_get_constraintdef(c.oid)
        FROM pg_constraint c
        WHERE conrelid = 'account_offices'::regclass
    """).fetchall()
    for r in rows:
        print(r["conname"], ":", r["pg_get_constraintdef"])
    # Also check what source values exist
    vals = c.execute("SELECT DISTINCT source FROM account_offices WHERE source IS NOT NULL").fetchall()
    print("Existing source values:", [r["source"] for r in vals])
