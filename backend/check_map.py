import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check geocoded counts by office_type
    rows = c.execute("""
        SELECT office_type, source,
               count(*) total,
               count(lat) geocoded
        FROM account_offices
        WHERE NOT deleted
        GROUP BY office_type, source
        ORDER BY office_type, source
    """).fetchall()
    print("Office counts:")
    for r in rows:
        print(f"  {r['office_type']}/{r['source']}: {r['total']} total, {r['geocoded']} geocoded")

    # Check what the map API actually queries
    # Sample a geocoded Company office
    sample = c.execute("""
        SELECT o.office_type, o.lat, o.lng, o.address, o.city, a.name
        FROM account_offices o JOIN accounts a ON a.id = o.account_id
        WHERE o.lat IS NOT NULL AND o.office_type = 'Company'
        LIMIT 3
    """).fetchall()
    print("\nSample Company offices with coords:")
    for r in sample: print(f"  {r['name']}: {r['address']}, {r['city']} ({r['lat']},{r['lng']})")

    # Check what map endpoint filters on
    nearby = c.execute("""
        SELECT count(*) n FROM account_offices o
        WHERE NOT o.deleted AND o.lat IS NOT NULL
          AND o.office_type IN ('Company','HQ','Billing','Home','Other')
    """).fetchone()
    print(f"\nOffices matching old map filter: {nearby['n']}")

    nearby2 = c.execute("""
        SELECT count(*) n FROM account_offices o
        WHERE NOT o.deleted AND o.lat IS NOT NULL
    """).fetchone()
    print(f"All geocoded offices: {nearby2['n']}")
