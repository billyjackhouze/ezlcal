import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    c.execute("ALTER TABLE staff ADD COLUMN IF NOT EXISTS cal_color TEXT")
    c.commit()
    print("OK: cal_color column added")
