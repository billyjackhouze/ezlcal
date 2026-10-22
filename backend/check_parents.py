import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    for term in ["white water", "wwm", "energy transfer", "mastec", "primoris"]:
        rows = c.execute(
            "SELECT id, name, types FROM accounts WHERE name ILIKE %s ORDER BY name",
            (f"%{term}%",)
        ).fetchall()
        print(f"\n--- {term} ---")
        for r in rows: print(f"  {r['name']!r} ({r['types']})")
