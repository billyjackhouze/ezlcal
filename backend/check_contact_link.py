import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Sample buyer_names from account_quotes
    rows = c.execute("""
        SELECT DISTINCT buyer_name, account_id, COUNT(*) cnt, SUM(total_amount) total
        FROM account_quotes
        WHERE record_type='job' AND job_date >= '2026-01-01'
          AND buyer_name != ''
        GROUP BY buyer_name, account_id
        ORDER BY total DESC LIMIT 15
    """).fetchall()
    print("Top buyer names in jobs:")
    for r in rows:
        print(f"  {r['buyer_name']}: {r['cnt']} jobs ${float(r['total']):,.0f}")

    # Check if any match contact names
    rows2 = c.execute("""
        SELECT c.name, ca.account_id,
               COUNT(aq.id) as job_count,
               SUM(aq.total_amount) as total
        FROM contacts c
        JOIN contact_accounts ca ON ca.contact_id=c.id
        JOIN account_quotes aq ON aq.account_id=ca.account_id
          AND LOWER(TRIM(aq.buyer_name)) = LOWER(TRIM(c.name))
          AND aq.record_type='job'
          AND aq.job_date >= '2026-01-01'
        GROUP BY c.name, ca.account_id
        ORDER BY total DESC LIMIT 10
    """).fetchall()
    print(f"\nContacts matched by buyer_name ({len(rows2)}):")
    for r in rows2:
        print(f"  {r['name']}: {r['job_count']} jobs ${float(r['total']):,.0f}")
