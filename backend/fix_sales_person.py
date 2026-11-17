import psycopg, os, json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

MAPPINGS = [
    # (match variants, correct account name)
    # Adonis
    ("Adonis Gonzalez", "ADONIS"),
    ("Adones Gonzalez", "ADONIS"),
    ("Adonis Gonzaqlez", "ADONIS"),
    ("Adonis", "ADONIS"),
    # Joey Vela
    ("Joseph Vela", "jvela"),
    ("Joseph  Vela", "jvela"),  # double space
    ("Vela, Joseph", "jvela"),
    ("Vela,Joseph", "jvela"),
    ("jvela", "jvela"),  # already correct but normalize case
    # Trey Palmer
    ("TPalmer", "tpalmer"),
    ("TPALMER", "tpalmer"),
    # Tim Green
    ("TGREEN", "tgreen"),
]

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    # 1. Backup affected rows BEFORE changes
    affected_variants = [m[0] for m in MAPPINGS]
    placeholders = ",".join(["%s"] * len(affected_variants))
    backup_rows = c.execute(
        f"SELECT id, job_number, sales_person, record_type, job_date, quote_date "
        f"FROM account_quotes WHERE sales_person IN ({placeholders})",
        affected_variants
    ).fetchall()
    
    backup_file = Path(r"C:\Apps\ezlcal\backend\sales_person_backup.json")
    backup_data = {
        "backup_time": datetime.now().isoformat(),
        "row_count": len(backup_rows),
        "rows": [dict(r) for r in backup_rows]
    }
    # Convert dates to strings for JSON
    for row in backup_data["rows"]:
        for k, v in row.items():
            if hasattr(v, 'isoformat'):
                row[k] = v.isoformat()
    
    backup_file.write_text(json.dumps(backup_data, indent=2), encoding="utf-8")
    print(f"Backed up {len(backup_rows)} rows to {backup_file}")
    
    # 2. Show preview
    print("\nChanges to be made:")
    for variant, correct in MAPPINGS:
        n = c.execute(
            "SELECT COUNT(*) n FROM account_quotes WHERE sales_person = %s",
            (variant,)
        ).fetchone()["n"]
        if n > 0:
            arrow = "" if variant == correct else f" -> {correct}"
            print(f"  '{variant}'{arrow}: {n} records")
    
    # 3. Apply
    total = 0
    for variant, correct in MAPPINGS:
        if variant == correct:
            continue
        n = c.execute(
            "UPDATE account_quotes SET sales_person = %s WHERE sales_person = %s",
            (correct, variant)
        ).rowcount
        if n > 0:
            print(f"  Updated {n} rows: '{variant}' -> '{correct}'")
        total += n
    
    c.commit()
    print(f"\nDone. {total} records updated.")
    print(f"Rollback file: {backup_file}")
    print("To rollback: run restore_sales_person.py")

# Also write rollback script
rollback = r"""
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
"""
Path(r"C:\Apps\ezlcal\backend\restore_sales_person.py").write_text(rollback, encoding="utf-8")
print("Rollback script written to restore_sales_person.py")
