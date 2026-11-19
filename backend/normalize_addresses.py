import psycopg, os, re
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

ABBREVS = [
    (r'\bAve\.?\b', 'Avenue'),
    (r'\bBlvd\.?\b', 'Boulevard'),
    (r'\bSt\.?\b', 'Street'),
    (r'\bDr\.?\b', 'Drive'),
    (r'\bRd\.?\b', 'Road'),
    (r'\bLn\.?\b', 'Lane'),
    (r'\bCt\.?\b', 'Court'),
    (r'\bPkwy\.?\b', 'Parkway'),
    (r'\bHwy\.?\b', 'Highway'),
    (r'\bFwy\.?\b', 'Freeway'),
    (r'\bSte\.?\b', 'Suite'),
    (r'\bN\.(?=\s)', 'North'),
    (r'\bS\.(?=\s)', 'South'),
    (r'\bE\.(?=\s)', 'East'),
    (r'\bW\.(?=\s)', 'West'),
]

def normalize(addr):
    if not addr: return addr
    a = addr.strip()
    for pattern, replacement in ABBREVS:
        a = re.sub(pattern, replacement, a, flags=re.IGNORECASE)
    a = re.sub(r'\b(Avenue|Boulevard|Street|Drive|Road|Lane|Court|Parkway|Highway|Suite)\.', 
               lambda m: m.group(1), a, flags=re.IGNORECASE)
    return ' '.join(a.split())

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT id, address FROM account_offices
        WHERE office_type = 'Company' AND NOT deleted
    """).fetchall()

    changes = [(r["id"], r["address"], normalize(r["address"]))
               for r in rows if normalize(r["address"]) != r["address"]]

    print(f"Would update {len(changes)} of {len(rows)} Company addresses")
    print("\nSample changes (first 30):")
    for _, old, new in changes[:30]:
        print(f"  {repr(old)}")
        print(f"  -> {repr(new)}")
        print()

    ans = input(f"\nApply {len(changes)} updates? (YES to confirm): ")
    if ans.strip() == "YES":
        updated = 0
        for id_, _, new_addr in changes:
            c.execute("UPDATE account_offices SET address=%s, updated_at=now() WHERE id=%s",
                      (new_addr, id_))
            updated += 1
        print(f"Done: {updated} addresses normalized")
    else:
        print("Aborted")
