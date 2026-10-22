import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    total = c.execute("SELECT count(*) FROM accounts").fetchone()["count"]
    with_parent = c.execute("SELECT count(*) FROM accounts WHERE parent_id IS NOT NULL").fetchone()["count"]
    with_root = c.execute("SELECT count(*) FROM accounts WHERE root_id IS NOT NULL").fetchone()["count"]
    print(f"Total accounts: {total}")
    print(f"With parent_id: {with_parent}")
    print(f"With root_id:   {with_root}")
    print()
    # White Water family
    rows = c.execute(
        "SELECT a.name, a.types, a.parent_id, p.name AS parent_name"
        " FROM accounts a LEFT JOIN accounts p ON p.id = a.parent_id"
        " WHERE a.root_id = (SELECT id FROM accounts WHERE name = %s AND types = %s LIMIT 1)"
        " ORDER BY a.parent_id NULLS FIRST, a.name",
        ("White Water Midstream", "CU")
    ).fetchall()
    print("White Water Midstream family:")
    for r in rows:
        print(f"  {r['name']!r} ({r['types']}) parent={r['parent_name']!r}")
    print()
    # Energy Transfer family
    rows = c.execute(
        "SELECT a.name, a.types, p.name AS parent_name"
        " FROM accounts a LEFT JOIN accounts p ON p.id = a.parent_id"
        " WHERE a.root_id = (SELECT id FROM accounts WHERE name = %s LIMIT 1)"
        " ORDER BY a.name",
        ("ENERGY TRANSFER",)
    ).fetchall()
    print("Energy Transfer family:")
    for r in rows:
        print(f"  {r['name']!r} ({r['types']}) parent={r['parent_name']!r}")
