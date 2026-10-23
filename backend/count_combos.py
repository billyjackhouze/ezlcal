import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    n = c.execute("""
        SELECT count(DISTINCT (trim(city), trim(state)))
        FROM account_offices
        WHERE NOT deleted AND lat IS NULL
          AND trim(city) != '' AND trim(state) != ''
    """).fetchone()["count"]
    print(f"Unique city/state combos: {n}")
    print(f"At 1.1 sec each = {n*1.1/60:.0f} minutes")
