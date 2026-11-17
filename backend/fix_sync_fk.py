from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\sync_quotes.py")
src = f.read_text(encoding="utf-8")

# Find the executemany and add ON CONFLICT skip for missing accounts
# The fix: filter rows to only those with account_ids that exist in accounts table
old = "Upserting {len(rows_to_upsert)} rows ({skipped} skipped)..."
print("checking...")

# Find the upsert section
idx = src.find("Upserting")
print(repr(src[idx-200:idx+100]))
