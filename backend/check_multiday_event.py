import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT title, date, end_date, start_time, end_time 
        FROM events 
        WHERE end_date IS NOT NULL AND NOT deleted
        ORDER BY date DESC LIMIT 5
    """).fetchall()
    for r in rows: print(dict(r))
