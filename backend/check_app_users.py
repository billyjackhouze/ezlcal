import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    cols = c.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='app_users' ORDER BY ordinal_position").fetchall()
    print("app_users columns:")
    for r in cols: print(f"  {r['column_name']}: {r['data_type']}")
    rows = c.execute("SELECT id, username, display_name, staff_id, is_admin FROM app_users LIMIT 3").fetchall()
    print("sample:", rows)
