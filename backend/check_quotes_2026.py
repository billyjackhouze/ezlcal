import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check quotes with 2026 dates
    r = c.execute("""
        SELECT COUNT(*) cnt, SUM(total_amount) total
        FROM account_quotes
        WHERE record_type='quote'
          AND COALESCE(quote_date, job_date) >= '2026-01-01'
          AND COALESCE(quote_date, job_date) < '2027-01-01'
    """).fetchone()
    print("2026 quotes:", dict(r))

    # Check top accounts by quotes
    rows = c.execute("""
        SELECT a.name,
               COUNT(*) cnt,
               SUM(aq.total_amount) total
        FROM account_quotes aq
        JOIN accounts a ON a.id=aq.account_id
        WHERE aq.record_type='quote'
          AND COALESCE(aq.quote_date,aq.job_date) >= '2026-01-01'
        GROUP BY a.name
        ORDER BY total DESC LIMIT 5
    """).fetchall()
    print("\nTop accounts by 2026 quotes:")
    for r in rows: print(f"  {r['name']}: {r['cnt']} quotes ${float(r['total']):,.0f}")

    # Check what years quotes exist in
    rows2 = c.execute("""
        SELECT date_part('year', COALESCE(quote_date,job_date)) yr,
               COUNT(*) cnt
        FROM account_quotes WHERE record_type='quote'
          AND COALESCE(quote_date,job_date) IS NOT NULL
        GROUP BY yr ORDER BY yr DESC LIMIT 8
    """).fetchall()
    print("\nQuotes by year:")
    for r in rows2: print(f"  {int(r['yr'])}: {r['cnt']}")
