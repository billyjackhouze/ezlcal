import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # How does the map API query offices?
    # Check a known company - Whitewater Midstream
    rows = c.execute("""
        SELECT ao.office_type, ao.notes, ao.address, ao.city, ao.state, ao.lat, ao.lng,
               a.name
        FROM account_offices ao
        JOIN accounts a ON a.id = ao.account_id
        WHERE a.name ILIKE '%whitewater%'
        ORDER BY ao.office_type
        LIMIT 10
    """).fetchall()
    for r in rows: print(dict(r))
    print()
    # Count distinct addresses per type
    rows2 = c.execute("""
        SELECT office_type,
               COUNT(*) total,
               COUNT(DISTINCT address||city||state) distinct_addrs
        FROM account_offices
        WHERE lat IS NOT NULL
        GROUP BY office_type
    """).fetchall()
    for r in rows2: print(dict(r))
