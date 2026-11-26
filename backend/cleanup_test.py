import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    rows = c.execute("SELECT id, name FROM contacts WHERE name ILIKE '%billy jack%' OR name ILIKE '%jack houze%' OR name ILIKE '%sdfg%' ORDER BY id").fetchall()
    print(f"Test contacts: {len(rows)}")
    for r in rows: print(f"  {r[0]} {r[1]}")
    ids = [r[0] for r in rows]
    if ids:
        c.execute("DELETE FROM contact_accounts WHERE contact_id = ANY(%s)", (ids,))
        c.execute("DELETE FROM contacts WHERE id = ANY(%s)", (ids,))
        print(f"Deleted {len(ids)}")
