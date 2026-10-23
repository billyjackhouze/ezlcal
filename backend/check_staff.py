import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check if cal_color column exists
    cols = c.execute("SELECT column_name FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position", ("staff",)).fetchall()
    print("staff columns:", [r["column_name"] for r in cols])
    # Sample staff IDs
    rows = c.execute("SELECT id, name FROM staff LIMIT 5").fetchall()
    print("Sample staff:")
    for r in rows: print(f"  {r['id']}: {r['name']}")
