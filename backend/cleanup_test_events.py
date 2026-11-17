import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("SELECT id, title, date, end_date, start_time FROM events WHERE title ILIKE %s OR title ILIKE %s ORDER BY date DESC", ("%test%", "%multi%")).fetchall()
    for r in rows:
        print(dict(r))
