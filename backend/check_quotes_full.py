import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Counts by record type
    types = c.execute("SELECT record_type, COUNT(*) n FROM account_quotes GROUP BY record_type ORDER BY n DESC").fetchall()
    print("=== By record_type ===")
    for r in types: print(f"  {r['record_type']}: {r['n']}")

    # Date range
    dates = c.execute("SELECT MIN(quote_date) mn, MAX(quote_date) mx, MIN(job_date) jmn, MAX(job_date) jmx FROM account_quotes").fetchone()
    print(f"\nQuote dates: {dates['mn']} to {dates['mx']}")
    print(f"Job dates:   {dates['jmn']} to {dates['jmx']}")

    # Null checks - what fields are missing data
    nulls = c.execute("""
        SELECT 
            COUNT(*) total,
            COUNT(sales_person) has_sales,
            COUNT(buyer_name) has_buyer,
            COUNT(project) has_project,
            COUNT(po_number) has_po,
            COUNT(invoice_number) has_invoice,
            COUNT(job_status) has_status,
            COUNT(clamps_total) has_clamps,
            COUNT(billing_address) has_addr
        FROM account_quotes
    """).fetchone()
    print(f"\nTotal: {nulls['total']}")
    print(f"Has sales_person: {nulls['has_sales']}")
    print(f"Has buyer_name:   {nulls['has_buyer']}")
    print(f"Has project:      {nulls['has_project']}")
    print(f"Has po_number:    {nulls['has_po']}")
    print(f"Has invoice_num:  {nulls['has_invoice']}")
    print(f"Has job_status:   {nulls['has_status']}")
    print(f"Has clamps_total: {nulls['has_clamps']}")
    print(f"Has billing_addr: {nulls['has_addr']}")

    # Sample job row
    sample = c.execute("SELECT * FROM account_quotes WHERE record_type='Job' LIMIT 1").fetchone()
    if sample:
        print("\nSample job:")
        for k,v in sample.items(): print(f"  {k}: {v}")
