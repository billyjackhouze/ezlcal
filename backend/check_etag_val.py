import psycopg, os, hashlib
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    stamp = c.execute(
        "SELECT (SELECT max(updated_at) FROM accounts)::text || (SELECT max(updated_at) FROM contacts)::text"
        " || (SELECT count(*) FROM staff WHERE active)::text || (SELECT count(*) FROM contact_accounts)::text"
        " || coalesce((SELECT max(updated_at) FROM account_offices)::text,'') || 'v4' AS s"
    ).fetchone()["s"]
    etag = '"' + hashlib.sha1((stamp or "").encode()).hexdigest()[:16] + '"'
    print("Current ETag:", etag)
