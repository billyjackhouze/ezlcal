import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) FROM accounts").fetchone()["count"]
    with_addr = c.execute(
        "SELECT count(*) FROM account_offices WHERE address IS NOT NULL AND address != ''"
    ).fetchone()["count"]
    geocoded = c.execute(
        "SELECT count(*) FROM account_offices WHERE lat IS NOT NULL"
    ).fetchone()["count"]
    offices = c.execute("SELECT count(*) FROM account_offices").fetchone()["count"]
    print(f"Accounts: {total}")
    print(f"Offices total: {offices}")
    print(f"Offices with address: {with_addr}")
    print(f"Offices geocoded: {geocoded}")
    print()
    rows = c.execute(
        "SELECT o.address, o.city, o.state, o.lat, o.lng, a.name"
        " FROM account_offices o JOIN accounts a ON a.id = o.account_id"
        " WHERE o.address IS NOT NULL AND o.address != ''"
        " LIMIT 10"
    ).fetchall()
    print("Sample offices with addresses:")
    for r in rows:
        print(f"  {r['name']}: {r['address']}, {r['city']}, {r['state']} lat={r['lat']}")
