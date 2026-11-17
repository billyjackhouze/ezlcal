import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # Most recent records synced
    recent = c.execute("""
        SELECT MAX(updated_at) last_sync, COUNT(*) n
        FROM account_quotes
        WHERE updated_at > now() - interval '7 days'
    """).fetchone()
    print(f"Last 7 days: {recent['n']} records, last update: {recent['last_sync']}")

    # Date range of data
    dates = c.execute("""
        SELECT MIN(updated_at) first, MAX(updated_at) last FROM account_quotes
    """).fetchone()
    print(f"Data range: {dates['first']} to {dates['last']}")

    # Check FM_HOST in env
    print(f"FM_HOST: {os.environ.get('FM_HOST','not set')}")
    print(f"FM_DB: {os.environ.get('FM_DB','not set')}")
