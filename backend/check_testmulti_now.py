import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    r = c.execute("""
        SELECT title, date, end_date, start_time, end_time
        FROM events WHERE title='Test Multi' AND NOT deleted
    """).fetchone()
    print(dict(r))
