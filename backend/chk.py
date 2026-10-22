import psycopg, os
from dotenv import load_dotenv
load_dotenv('.env')
with psycopg.connect(os.environ['DATABASE_URL']) as c:
    total = c.execute('SELECT count(*) FROM accounts').fetchone()[0]
    with_city = c.execute("SELECT count(*) FROM accounts WHERE city != ''").fetchone()[0]
    with_addr = c.execute("SELECT count(*) FROM accounts WHERE address != '' OR city != ''").fetchone()[0]
    sample = c.execute("SELECT name, address, city, state FROM accounts WHERE city != '' LIMIT 5").fetchall()
    print(f'Total: {total}')
    print(f'With city: {with_city}')
    print(f'With address or city: {with_addr}')
    for r in sample: print(' ', r)
