import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Find Whitewater
    rows = c.execute("""
        SELECT id, name, sales_ytd, parent_id, root_id
        FROM accounts WHERE name ILIKE '%white%water%'
        OR name ILIKE '%whitewater%'
    """).fetchall()
    print("Whitewater matches:", len(rows))
    for r in rows: print(" ", dict(r))

    # What sales columns exist?
    cols = c.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='accounts' AND column_name ILIKE '%sale%'
        ORDER BY column_name
    """).fetchall()
    print("\nSales columns:", [r['column_name'] for r in cols])

    # Top 5 accounts by sales_ytd
    top = c.execute("""
        SELECT name, sales_ytd, parent_id, root_id
        FROM accounts WHERE sales_ytd > 0
        ORDER BY sales_ytd DESC LIMIT 5
    """).fetchall()
    print("\nTop 5 by sales_ytd:")
    for r in top: print(" ", dict(r))
