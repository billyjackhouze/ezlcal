import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    types = c.execute("SELECT office_type, COUNT(*) as n FROM account_offices WHERE NOT deleted GROUP BY office_type ORDER BY n DESC").fetchall()
    for r in types: print(dict(r))
