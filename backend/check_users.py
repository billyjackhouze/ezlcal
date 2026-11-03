import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    cols = c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position").fetchall()
    print("users columns:", [r["column_name"] for r in cols])
    rows = c.execute("SELECT id, username, display_name, default_tab, cal_default FROM users LIMIT 3").fetchall()
    print("sample:", rows)
