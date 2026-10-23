import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check orphaned offices (account_id not in accounts)
    orphans = c.execute("""
        SELECT count(*) FROM account_offices o
        WHERE NOT o.deleted AND o.lat IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM accounts a WHERE a.id = o.account_id)
    """).fetchone()["count"]
    # Check how many offices the map query actually returns
    valid = c.execute("""
        SELECT count(*) FROM account_offices o
        JOIN accounts a ON a.id = o.account_id
        WHERE NOT o.deleted AND o.lat IS NOT NULL
    """).fetchone()["count"]
    print(f"Geocoded offices: 8717")
    print(f"Orphaned (no account): {orphans}")
    print(f"Valid (join succeeds): {valid}")
    # Sample valid office
    row = c.execute("""
        SELECT o.account_id, o.lat, o.lng, a.name, a.types
        FROM account_offices o
        JOIN accounts a ON a.id = o.account_id
        WHERE NOT o.deleted AND o.lat IS NOT NULL
        LIMIT 1
    """).fetchone()
    print(f"Sample: {row}")
