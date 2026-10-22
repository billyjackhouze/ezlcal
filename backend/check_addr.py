import psycopg, os
from dotenv import load_dotenv
load_dotenv(r'C:\apps\ezlcal\backend\.env')
with psycopg.connect(os.environ['DATABASE_URL']) as c:
    total = c.execute('SELECT count(*) FROM accounts').fetchone()[0]
    with_addr = c.execute("SELECT count(*) FROM accounts WHERE address != '' OR city != ''").fetchone()[0]
    sample = c.execute("SELECT name, address, city, state FROM accounts WHERE city != '' LIMIT 5").fetchall()
    print(f'Total accounts: {total}')
    print(f'With address/city: {with_addr}')
    print('Samples:')
    for r in sample: print(' ', r)
