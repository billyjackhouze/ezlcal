from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

old = """            FROM account_offices o
            JOIN accounts a ON a.id = o.account_id
            WHERE NOT o.deleted
              AND o.lat IS NOT NULL
            ORDER BY a.name, o.office_type"""

new = """            FROM account_offices o
            JOIN accounts a ON a.id = o.account_id
            WHERE NOT o.deleted
              AND o.lat IS NOT NULL
              AND o.office_type = 'Company'
            ORDER BY a.name, o.office_type"""

if old in src:
    src = src.replace(old, new, 1)
    print("OK: map filtered to Company only")
else:
    print("MISS")

f.write_text(src, encoding="utf-8")
print("Done")
