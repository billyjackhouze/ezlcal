import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted").fetchone()["count"]
    geocoded = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NOT NULL").fetchone()["count"]
    skipped = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NOT NULL").fetchone()["count"]
    remaining = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NULL").fetchone()["count"]
    print(f"Total offices:   {total}")
    print(f"Geocoded (pins): {geocoded}")
    print(f"Skipped (dirty): {skipped}")
    print(f"Still pending:   {remaining}")
