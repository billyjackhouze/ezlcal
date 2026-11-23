import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Check quote dates
    r = c.execute("""
        SELECT COUNT(*) total,
               COUNT(quote_date) with_date,
               COUNT(job_date) with_job_date,
               SUM(total_amount) total_amt
        FROM account_quotes WHERE record_type='quote'
    """).fetchone()
    print("Quotes:", dict(r))

    # Check contact_accounts - how are contacts linked to sales?
    r2 = c.execute("""
        SELECT COUNT(*) total,
               COUNT(NULLIF(sales_ytd,0)) with_sales
        FROM contact_accounts
    """).fetchone()
    print("contact_accounts:", dict(r2))

    # How does the sync populate contact sales?
    # Check if there is a sales_person field we could use
    r3 = c.execute("""
        SELECT sales_person, COUNT(*) cnt, SUM(total_amount) total
        FROM account_quotes
        WHERE record_type='job'
          AND date_part('year',job_date)=2026
        GROUP BY sales_person ORDER BY total DESC LIMIT 10
    """).fetchall()
    print("\nSales by person 2026:")
    for r in r3: print(f"  {r['sales_person']}: {r['cnt']} jobs ${float(r['total']):,.0f}")
