import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    c.execute("UPDATE account_offices SET updated_at=now() WHERE id=(SELECT id FROM account_offices LIMIT 1)")
    print("Done")
