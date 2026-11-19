import psycopg, os, re
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

# Abbreviation patterns to normalize
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
    (r'\bN\.?\b', 'North'),
    (r'\bS\.?\b', 'South'),
    (r'\bE\.?\b', 'East'),
    (r'\bW\.?\b', 'West'),
    (r'\bSte\.?\b', 'Suite'),
]

def normalize(addr):
    if not addr: return addr
    a = addr.strip()
    for pattern, replacement in ABBREVS:
        a = re.sub(pattern, replacement, a, flags=re.IGNORECASE)
    return ' '.join(a.split())  # collapse whitespace

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    rows = c.execute("""
        SELECT id, account_id, address, city, state
        FROM account_offices
        WHERE office_type = 'Company' AND NOT deleted
        ORDER BY address
        LIMIT 500
    """).fetchall()

    changed = [(r["id"], r["address"], normalize(r["address"])) 
               for r in rows if normalize(r["address"]) != r["address"]]
    
    print(f"Would normalize {len(changed)} of {len(rows)} sampled records")
    for id_, old, new in changed[:20]:
        print(f"  {repr(old)} -> {repr(new)}")
