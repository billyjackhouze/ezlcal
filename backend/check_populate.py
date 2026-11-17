import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check accounts table
    accts = c.execute("SELECT COUNT(*) as n FROM accounts").fetchone()["n"]
    print(f"Accounts: {accts}")
    # Check offices by source
    by_source = c.execute("SELECT source, COUNT(*) as n FROM account_offices GROUP BY source").fetchall()
    print("Offices by source:", [dict(r) for r in by_source])
    # Check if geocode_retry exists
    print("populate_offices exists:", Path(r"C:\Apps\ezlcal\backend\populate_offices.py").exists())
    print("geocode_retry exists:", Path(r"C:\Apps\ezlcal\backend\geocode_retry.py").exists())
    # Sample an office with no lat
    sample = c.execute("SELECT id, office_type, address, city, state, zip FROM account_offices WHERE lat IS NULL AND address IS NOT NULL AND address != '' LIMIT 3").fetchall()
    print("Sample ungeocoded:", [dict(r) for r in sample])
