import psycopg, os, urllib.request, json
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    ct = c.execute("SELECT id, name FROM contacts WHERE upper(name) LIKE %s LIMIT 1", ("%BRADLEY WYATT%",)).fetchone()
    print("Contact:", ct)
    if ct:
        cid = ct["id"]
        # Check jobs match in DB directly
        rows = c.execute("SELECT count(*) n FROM account_quotes WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type=%s", (ct["name"],"job")).fetchone()
        print("Jobs in DB for this buyer:", rows["n"])
        rows2 = c.execute("SELECT count(*) n FROM account_quotes WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type=%s", (ct["name"],"quote")).fetchone()
        print("Quotes in DB for this buyer:", rows2["n"])
        # Check what record_type values exist
        types = c.execute("SELECT DISTINCT record_type FROM account_quotes LIMIT 5").fetchall()
        print("Record types:", [r["record_type"] for r in types])
