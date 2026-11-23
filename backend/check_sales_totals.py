import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check Whitewater - direct sales vs with subsidiaries
    r = c.execute("""
        SELECT id, name, sales_ytd, parent_id, root_id
        FROM accounts WHERE name ILIKE '%whitewater%'
    """).fetchone()
    print("Whitewater:", dict(r))
    
    # Check its children
    children = c.execute("""
        SELECT id, name, sales_ytd, parent_id, root_id
        FROM accounts WHERE parent_id = %s OR root_id = %s
    """, (r['id'], r['id'])).fetchall()
    print(f"\nChildren/subsidiaries: {len(children)}")
    for c2 in children[:10]: print(" ", dict(c2))
    
    # What columns does accounts table have for sales?
    cols = c.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='accounts' AND column_name ILIKE '%sales%'
        ORDER BY column_name
    """).fetchall()
    print("\nSales columns:", [r['column_name'] for r in cols])
