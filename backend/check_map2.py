import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NOT NULL").fetchone()["count"]
    houston = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NOT NULL AND city ILIKE %s AND state = %s", ("houston", "TX")).fetchone()["count"]
    sample = c.execute("SELECT account_id, address, city, state, lat, lng FROM account_offices WHERE NOT deleted AND lat IS NOT NULL AND state = %s LIMIT 3", ("TX",)).fetchall()
    print(f"Total geocoded offices: {total}")
    print(f"Houston TX offices: {houston}")
    print("Sample TX:")
    for r in sample: print(" ", r)
