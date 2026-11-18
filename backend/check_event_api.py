import urllib.request, json, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

# Check what the events API returns for this event
import psycopg
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check how events are returned from the API
    r = c.execute("""
        SELECT id, title, date::text, end_date::text, start_time, end_time
        FROM events 
        WHERE id = 'e3c336a8-7e87-478f-8412-51ed0d641b39'
    """).fetchone()
    print("DB row:", dict(r))
    
    # Check the API response format - find how events endpoint serializes
    src = Path(r"C:\Apps\ezlcal\backend\app\main.py").read_text(encoding="utf-8")
    idx = src.find('"time"')
    while idx >= 0:
        print("time field:", repr(src[max(0,idx-20):idx+60]))
        idx = src.find('"time"', idx+1)
        if idx > 5000: break
