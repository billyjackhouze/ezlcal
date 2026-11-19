import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # What office_types exist and how many of each
    rows = c.execute("""
        SELECT office_type, source, COUNT(*) as cnt,
               COUNT(lat) as geocoded
        FROM account_offices
        GROUP BY office_type, source
        ORDER BY cnt DESC
    """).fetchall()
    for r in rows: print(dict(r))
    print()
    # Sample some ship-to records
    rows2 = c.execute("""
        SELECT office_type, notes, address, city, state, lat, lng
        FROM account_offices
        WHERE notes ILIKE '%ship%' OR office_type ILIKE '%ship%'
        LIMIT 5
    """).fetchall()
    print("Ship-to samples:")
    for r in rows2: print(dict(r))
