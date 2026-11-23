import psycopg, os, json
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT a.id, a.name, a.types, a.parent_id, a.root_id,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS sales_ytd,
               COALESCE(SUM(CASE WHEN aq.record_type='job' AND date_part('year',aq.job_date)=date_part('year',now())-1 THEN aq.total_amount ELSE 0 END),0) AS sales_py,
               COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd,
               a.last_order, a.address, a.city, a.state, a.zip, a.homepage
        FROM accounts a
        LEFT JOIN account_quotes aq ON aq.account_id=a.id
        GROUP BY a.id, a.name, a.types, a.parent_id, a.root_id, a.last_order, a.address, a.city, a.state, a.zip, a.homepage
        ORDER BY a.name
    """).fetchall()
    
    # Check Williams Field Services row
    wfs = next((r for r in rows if 'WILLIAMS FIELD' in r['name']), None)
    print("WFS row:", dict(wfs) if wfs else "NOT FOUND")
    
    # Count non-zero quotes
    nonzero = sum(1 for r in rows if float(r['quotes_ytd']) > 0)
    print(f"\nTotal accounts: {len(rows)}, with quotes: {nonzero}")
    
    # Build array as API does
    arr = [[r["id"], r["name"], r["types"], r["parent_id"], r["root_id"],
            float(r["sales_ytd"]), float(r["sales_py"]), float(r["quotes_ytd"]),
            r["last_order"].isoformat() if r["last_order"] else None,
            r["address"], r["city"], r["state"], r["zip"], r["homepage"]]
           for r in rows]
    
    # Find WFS in arr
    wfs_arr = next((a for a in arr if 'WILLIAMS FIELD' in a[1]), None)
    print(f"\nWFS array[7] (quotes_ytd): {wfs_arr[7] if wfs_arr else 'NOT FOUND'}")
