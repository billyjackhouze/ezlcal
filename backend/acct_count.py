import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) FROM accounts").fetchone()["count"]
    dups = c.execute("SELECT count(*) FROM (SELECT name FROM accounts GROUP BY name HAVING count(*) > 1) x").fetchone()["count"]
    parents = c.execute("SELECT count(*) FROM accounts WHERE parent_id IS NOT NULL").fetchone()["count"]
    print(f"Accounts: {total}")
    print(f"Duplicate name groups: {dups}")
    print(f"With parent_id: {parents}")
