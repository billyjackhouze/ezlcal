import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Get White Water Midstream family
    root = c.execute("SELECT id, name FROM accounts WHERE name = %s AND types = %s", ("White Water Midstream", "CU")).fetchone()
    if not root: root = c.execute("SELECT id, name FROM accounts WHERE name ILIKE %s ORDER BY length(coalesce(types,'')) DESC LIMIT 1", ("%White Water Midstream%",)).fetchone()
    print(f"Root: {root['name']} ({root['id']})")
    members = c.execute(
        "SELECT name, types, sales_ytd, sales_py FROM accounts WHERE root_id = %s OR id = %s ORDER BY name",
        (root['id'], root['id'])
    ).fetchall()
    ytd_total = sum(float(r['sales_ytd'] or 0) for r in members)
    py_total = sum(float(r['sales_py'] or 0) for r in members)
    print(f"\nFamily members ({len(members)}):")
    for r in members:
        print(f"  {r['name']}: YTD=${float(r['sales_ytd'] or 0):,.0f} PY=${float(r['sales_py'] or 0):,.0f}")
    print(f"\nFamily YTD total: ${ytd_total:,.0f}")
    print(f"Family PY total:  ${py_total:,.0f}")
