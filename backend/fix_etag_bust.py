from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

# Change the ETag version string to force cache bust
old = "|| coalesce((SELECT max(updated_at) FROM account_offices)::text,'') || 'v3' AS s"
new = "|| coalesce((SELECT max(updated_at) FROM account_offices)::text,'') || 'v4' AS s"
if old in src:
    src = src.replace(old, new, 1)
    print("OK: ETag version bumped to v4")
else:
    print("MISS")

f.write_text(src, encoding="utf-8")
print("Done")
