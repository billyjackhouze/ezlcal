import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) n FROM account_offices WHERE NOT deleted").fetchone()["n"]
    geocoded = c.execute("SELECT count(*) n FROM account_offices WHERE NOT deleted AND lat IS NOT NULL").fetchone()["n"]
    pending = c.execute("SELECT count(*) n FROM account_offices WHERE NOT deleted AND lat IS NULL").fetchone()["n"]
    print(f"Total: {total}, Geocoded: {geocoded}, Pending: {pending}")
