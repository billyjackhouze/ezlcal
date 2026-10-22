import psycopg, os
from dotenv import load_dotenv
load_dotenv('.env')
with psycopg.connect(os.environ['DATABASE_URL']) as c:
    rows = c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name").fetchall()
    for r in rows: print(r[0])
