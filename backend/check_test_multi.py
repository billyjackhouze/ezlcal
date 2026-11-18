import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT id, title, date, end_date, start_time, end_time, deleted
        FROM events WHERE title ILIKE '%test multi%' OR title ILIKE '%multi test%'
        ORDER BY date DESC
    """).fetchall()
    for r in rows: print(dict(r))
