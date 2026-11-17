import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    cols = c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='account_offices' ORDER BY ordinal_position").fetchall()
    print("Columns:", [r["column_name"] for r in cols])
    total = c.execute("SELECT COUNT(*) as n FROM account_offices").fetchone()["n"]
    geocoded = c.execute("SELECT COUNT(*) as n FROM account_offices WHERE lat IS NOT NULL").fetchone()["n"]
    print(f"Total: {total}, Geocoded: {geocoded}")
    sample = c.execute("SELECT * FROM account_offices WHERE lat IS NOT NULL LIMIT 2").fetchall()
    for r in sample: print(dict(r))
