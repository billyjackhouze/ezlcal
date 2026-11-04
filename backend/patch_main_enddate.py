from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

# 1. Add end_date to EventIn model
old = '    end: str = ""\n    cat: str = ""'
new = '    end: str = ""\n    endDate: str = ""\n    cat: str = ""'
assert old in src
src = src.replace(old, new, 1)
print("OK: EventIn")

# 2. Add end_date to SELECT
old = '"SELECT id,title,date,start_time,end_time,category,location,notes,deleted,updated_at,updated_by,created_by "'
new = '"SELECT id,title,date,end_date,start_time,end_time,category,location,notes,deleted,updated_at,updated_by,created_by "'
assert old in src
src = src.replace(old, new, 1)
print("OK: SELECT")

# 3. Add end_date to response dict
old = '"end": e["end_time"], "cat": e["category"]'
new = '"end": e["end_time"], "endDate": e["end_date"].isoformat() if e["end_date"] else "", "cat": e["category"]'
assert old in src
src = src.replace(old, new, 1)
print("OK: response dict")

# 4. Add end_date to INSERT
old = 'INSERT INTO events (id,title,date,start_time,end_time,category,location,notes,deleted,created_by,updated_by,updated_at)\n               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
new = 'INSERT INTO events (id,title,date,end_date,start_time,end_time,category,location,notes,deleted,created_by,updated_by,updated_at)\n               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
assert old in src
src = src.replace(old, new, 1)
print("OK: INSERT")

# 5. Add end_date to UPSERT SET
old = 'end_time=EXCLUDED.end_time,category=EXCLUDED.category'
new = 'end_date=EXCLUDED.end_date,end_time=EXCLUDED.end_time,category=EXCLUDED.category'
assert old in src
src = src.replace(old, new, 1)
print("OK: UPSERT")

# 6. Add end_date to params tuple
old = "(event_id, ev.title.strip()[:300], day, ev.time[:5], ev.end[:5], ev.cat[:"
new = "(event_id, ev.title.strip()[:300], day, ev.endDate[:10] if ev.endDate else None, ev.time[:5], ev.end[:5], ev.cat[:"
assert old in src
src = src.replace(old, new, 1)
print("OK: params")

f.write_text(src, encoding="utf-8")
print("Done")
