import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    rows = c.execute("SELECT id, name FROM contacts WHERE name ILIKE '%billy jack simpson%' ORDER BY id").fetchall()
    print(f"Found {len(rows)}:")
    for r in rows: print(f"  {r[0]}")
    if len(rows) > 1:
        keep_id = rows[-1][0]
        delete_ids = [r[0] for r in rows[:-1]]
        c.execute("DELETE FROM contact_accounts WHERE contact_id = ANY(%s)", (delete_ids,))
        c.execute("DELETE FROM contacts WHERE id = ANY(%s)", (delete_ids,))
        print(f"Kept {keep_id}, deleted {len(delete_ids)}")
