import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    by_type = c.execute("""
        SELECT office_type, 
               COUNT(*) as total,
               COUNT(lat) as geocoded,
               COUNT(CASE WHEN address IS NOT NULL AND address != '' THEN 1 END) as has_address
        FROM account_offices WHERE NOT deleted
        GROUP BY office_type ORDER BY office_type
    """).fetchall()
    for r in by_type: print(dict(r))
    # Sample buyer with address but no coords
    sample = c.execute("""
        SELECT address, city, state, zip FROM account_offices 
        WHERE office_type='Buyer' AND lat IS NULL 
        AND address IS NOT NULL AND address != '' LIMIT 3
    """).fetchall()
    print("Sample ungeocoded buyers:", [dict(r) for r in sample])
