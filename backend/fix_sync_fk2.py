from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\sync_quotes.py")
src = f.read_text(encoding="utf-8")

old = '    print(f"Upserting {len(upsert_rows)} rows ({skip} skipped)...")\n\n    with psycopg.connect(DB, row_factory=di'
new = ('    # Filter to only rows whose account_id exists in Postgres\n'
       '    with psycopg.connect(DB, row_factory=dict_row) as _c:\n'
       '        valid_ids = {r["id"] for r in _c.execute("SELECT id FROM accounts").fetchall()}\n'
       '    before = len(upsert_rows)\n'
       '    upsert_rows = [r for r in upsert_rows if r[1] in valid_ids]\n'
       '    skip += before - len(upsert_rows)\n'
       '    print(f"Upserting {len(upsert_rows)} rows ({skip} skipped, {before-len(upsert_rows)} missing account)...")\n\n'
       '    with psycopg.connect(DB, row_factory=di')

assert old in src, "Pattern not found"
src = src.replace(old, new, 1)
f.write_text(src, encoding="utf-8")

import ast
ast.parse(src)
print("OK - syntax valid")
