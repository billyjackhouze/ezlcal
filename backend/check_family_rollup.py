import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Find parent accounts that have children with sales
    rows = c.execute("""
        SELECT p.name, p.sales_ytd as own_sales,
               SUM(c.sales_ytd) as child_sales,
               COUNT(c.id) as child_count
        FROM accounts p
        JOIN accounts c ON c.root_id = p.id AND c.id != p.id
        WHERE c.sales_ytd > 0
        GROUP BY p.id, p.name, p.sales_ytd
        ORDER BY child_sales DESC
        LIMIT 10
    """).fetchall()
    print("Parents with children having sales:")
    for r in rows:
        print(f"  {r['name']}: own=${r['own_sales']:,.0f} children=${r['child_sales']:,.0f} ({r['child_count']} children)")
