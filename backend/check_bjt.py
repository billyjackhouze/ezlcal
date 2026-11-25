import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    r = c.execute("SELECT id, name, types FROM accounts WHERE name ILIKE '%billy jack%'").fetchall()
    for row in r: print(dict(row))
