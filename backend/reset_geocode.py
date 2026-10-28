import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    n = c.execute("""
        UPDATE account_offices SET geocoded_at=NULL, lat=NULL, lng=NULL
        WHERE source='fm' AND office_type IN ('Company','Buyer')
    """).rowcount
    c.commit()
    print(f"Reset {n} offices for geocoding")
    pending = c.execute("SELECT count(*) n FROM account_offices WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NULL").fetchone()["n"]
    print(f"Ready to geocode: {pending}")
