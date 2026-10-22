import psycopg, os
from dotenv import load_dotenv
load_dotenv('.env')
with psycopg.connect(os.environ['DATABASE_URL']) as c:
    # Check Bay Runner Pipeline quotes
    r = c.execute("SELECT id FROM accounts WHERE name ILIKE '%Bay Runner%'").fetchone()
    if r:
        aid = r[0]
        print('Account ID:', aid)
        q = c.execute("SELECT count(*) FROM account_quotes WHERE account_id=%s",(aid,)).fetchone()[0]
        print('Quotes/jobs count:', q)
        sample = c.execute("SELECT record_type, job_number, quote_date, total_amount FROM account_quotes WHERE account_id=%s LIMIT 3",(aid,)).fetchall()
        for row in sample: print(' ', row)
    else:
        print('Bay Runner not found')
    # Check index exists
    idx = c.execute("SELECT indexname FROM pg_indexes WHERE tablename='account_quotes'").fetchall()
    print('Indexes:', [r[0] for r in idx])
