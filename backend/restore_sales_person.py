
import psycopg, os, json
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
backup = json.loads(Path(r"C:\Apps\ezlcal\backend\sales_person_backup.json").read_text())
print(f"Restoring {backup['row_count']} rows from backup {backup['backup_time']}")
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    for row in backup["rows"]:
        c.execute("UPDATE account_quotes SET sales_person=%s WHERE id=%s",
                  (row["sales_person"], row["id"]))
    c.commit()
    print("Rollback complete.")
