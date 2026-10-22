import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute(
        "SELECT id, name, types, parent_id, root_id FROM accounts"
        " WHERE name ILIKE '%white water%' OR name ILIKE '%whitewater%'"
        " ORDER BY name"
    ).fetchall()
    print("White Water accounts:")
    for r in rows: print(" ", r)
    print()
    ct = c.execute("SELECT count(*) FROM accounts WHERE parent_id IS NOT NULL").fetchone()["count"]
    total = c.execute("SELECT count(*) FROM accounts").fetchone()["count"]
    print(f"Accounts with parent_id: {ct} of {total}")
    print()
    dups = c.execute(
        "SELECT name, count(*) as cnt FROM accounts"
        " GROUP BY name HAVING count(*) > 1"
        " ORDER BY cnt DESC LIMIT 20"
    ).fetchall()
    print("Top duplicate account names:")
    for r in dups: print(f"  {r['name']}: {r['cnt']}")
