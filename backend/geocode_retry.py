import csv, os, time, urllib.request
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
DB = os.environ["DATABASE_URL"]
URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
CHUNK = 2000

def census_batch(rows):
    lines = ["Unique ID,Street address,City,State,ZIP"]
    for oid, addr, city, state, zip_ in rows:
        addr  = (addr  or "").replace(",","").replace('"',"").replace("\r","").replace("\n","")[:100]
        city  = (city  or "").replace(",","").replace('"',"")[:50]
        state = (state or "").replace(",","").replace('"',"")[:2]
        zip_  = (zip_  or "").replace(",","").replace('"',"")[:10]
        if city and state:
            lines.append(f'"{oid}","{addr}","{city}","{state}","{zip_}"')
    if len(lines) <= 1:
        return {}
    body = "\n".join(lines).encode("utf-8")
    boundary = "CensusBatch"
    parts = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"benchmark\"\r\n\r\nPublic_AR_Current\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"addressFile\"; filename=\"addr.csv\"\r\nContent-Type: text/plain\r\n\r\n"
    ).encode() + body + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(URL, data=parts,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "User-Agent": "ezlcal/1.0"}, method="POST")
    results = {}
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            text = r.read().decode("utf-8", errors="replace")
        for line in text.splitlines():
            p = next(csv.reader([line]))
            if len(p) >= 6 and p[2].strip().upper() == "MATCH":
                oid = p[0].strip().strip('"')
                coords = p[5].strip()
                if "," in coords:
                    try:
                        lng, lat = coords.split(",", 1)
                        results[oid] = (float(lat.strip()), float(lng.strip()))
                    except ValueError: pass
    except Exception as e:
        print(f"  error: {e}", flush=True)
        return None
    return results

with psycopg.connect(DB, row_factory=dict_row) as c:
    pending = c.execute("""
        SELECT id, address, city, state, zip FROM account_offices
        WHERE NOT deleted AND lat IS NULL
          AND trim(coalesce(city,'')) != ''
        ORDER BY office_type, city
    """).fetchall()

print(f"Pending: {len(pending)}", flush=True)
total_ok = total_fail = 0

for start in range(0, len(pending), CHUNK):
    chunk = pending[start:start+CHUNK]
    rows = [(r["id"],r["address"],r["city"],r["state"],r["zip"]) for r in chunk]
    batch_num = start//CHUNK+1
    total_batches = (len(pending)+CHUNK-1)//CHUNK
    print(f"Batch {batch_num}/{total_batches}: {len(rows)} addresses...", flush=True)
    matches = census_batch(rows)
    if matches is None:
        print(f"  Batch failed, marking skipped", flush=True)
        with psycopg.connect(DB, row_factory=dict_row) as c:
            for r in chunk:
                c.execute("UPDATE account_offices SET geocoded_at=now() WHERE id=%s",(r["id"],))
            c.commit()
        total_fail += len(chunk)
        continue
    print(f"  Matched: {len(matches)}/{len(rows)}", flush=True)
    with psycopg.connect(DB, row_factory=dict_row) as c:
        for r in chunk:
            if r["id"] in matches:
                lat, lng = matches[r["id"]]
                c.execute("UPDATE account_offices SET lat=%s,lng=%s,geocoded_at=now() WHERE id=%s",(lat,lng,r["id"]))
                total_ok += 1
            else:
                c.execute("UPDATE account_offices SET geocoded_at=now() WHERE id=%s",(r["id"],))
                total_fail += 1
        c.commit()
    print(f"  Running: {total_ok} geocoded", flush=True)
    time.sleep(1)

with psycopg.connect(DB, row_factory=dict_row) as c:
    n = c.execute("SELECT count(*) n FROM account_offices WHERE lat IS NOT NULL").fetchone()["n"]
print(f"\nDone. {total_ok} geocoded, {total_fail} unmatched. Total with coords: {n}", flush=True)
