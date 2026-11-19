import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Find duplicate addresses per account (same account, same address+city+state)
    rows = c.execute("""
        SELECT account_id, 
               lower(trim(address)) AS norm_addr,
               city, state,
               COUNT(*) AS cnt,
               array_agg(id ORDER BY id) AS ids
        FROM account_offices
        WHERE office_type = 'Company' AND NOT deleted
          AND address IS NOT NULL AND address != ''
        GROUP BY account_id, lower(trim(address)), city, state
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
        LIMIT 20
    """).fetchall()
    print(f"Duplicate address groups: {len(rows)}")
    for r in rows:
        print(f"  account={r['account_id']} addr={repr(r['norm_addr'])} city={r['city']} cnt={r['cnt']} ids={r['ids']}")
