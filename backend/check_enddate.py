import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check if end_date column exists
    cols = c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='events' ORDER BY ordinal_position").fetchall()
    print("events cols:", [r["column_name"] for r in cols])
    # Try adding it if missing
    c.execute("ALTER TABLE events ADD COLUMN IF NOT EXISTS end_date DATE")
    c.commit()
    print("end_date column ensured")
