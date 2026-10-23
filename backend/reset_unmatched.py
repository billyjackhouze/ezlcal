import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    n = c.execute("""
        UPDATE account_offices SET geocoded_at=NULL
        WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NOT NULL
          AND office_type = 'Billing'
          AND trim(coalesce(city,'')) != ''
    """).rowcount
    c.commit()
    print(f"Reset {n} offices for retry")
    remaining = c.execute("""
        SELECT count(*) FROM account_offices
        WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NULL
    """).fetchone()["count"]
    print(f"Ready to geocode: {remaining}")
