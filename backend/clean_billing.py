import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    n = c.execute("DELETE FROM account_offices WHERE office_type = 'Billing'").rowcount
    c.commit()
    print(f"Deleted {n} old Billing offices")
    totals = c.execute("SELECT office_type, count(*) n FROM account_offices WHERE NOT deleted GROUP BY office_type ORDER BY office_type").fetchall()
    for r in totals: print(f"  {r['office_type']}: {r['n']}")
