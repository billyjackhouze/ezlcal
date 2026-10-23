import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    n = c.execute("""
        UPDATE account_offices SET geocoded_at=now()
        WHERE NOT deleted AND lat IS NULL
          AND (
            trim(city) LIKE '%|%' OR
            trim(city) LIKE '%''%' OR
            trim(city) LIKE '%,%' OR
            trim(city) LIKE '%.%' OR
            length(trim(state)) > 3 OR
            trim(city) = '' OR trim(state) = ''
          )
    """).rowcount
    c.commit()
    print(f"Marked {n} dirty offices as geocoded (skipped)")
    remaining = c.execute("SELECT count(*) FROM account_offices WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NULL").fetchone()["count"]
    print(f"Remaining to geocode: {remaining}")
