import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT COUNT(*) as n FROM account_offices").fetchone()["n"]
    geocoded = c.execute("SELECT COUNT(*) as n FROM account_offices WHERE lat IS NOT NULL").fetchone()["n"]
    sample = c.execute("SELECT account_id, account_name, lat, lng, office_type FROM account_offices WHERE lat IS NOT NULL LIMIT 3").fetchall()
    print(f"Total offices: {total}, Geocoded: {geocoded}")
    for r in sample: print(dict(r))
