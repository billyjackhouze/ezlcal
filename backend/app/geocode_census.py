import csv, io, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DB = os.environ["DATABASE_URL"]
BATCH = 9000
URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"

def census_batch(rows):
    lines = ["Unique ID,Street address,City,State,ZIP"]
    for oid, addr, city, state, zip_ in rows:
        addr  = (addr  or "").replace(",","").replace('"',"")[:100]
        city  = (city  or "").replace(",","").replace('"',"")[:50]
        state = (state or "").replace(",","").replace('"',"")[:3]
        zip_  = (zip_  or "").replace(",","").replace('"',"")[:10]
        lines.append(f'"{oid}","{addr}","{city}","{state}","{zip_}"')
    body = "\n".join(lines).encode("utf-8")
    boundary = "CensusBatch"
    parts = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"benchmark\"\r\n\r\nPublic_AR_Current\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"addressFile\"; filename=\"addr.csv\"\r\nContent-Type: text/plain\r\n\r\n"
    ).encode() + body + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(URL, data=parts,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "User-Agent": "ezlcal/1.0"},method="POST")
    results = {}
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            text = r.read().decode("utf-8", errors="replace")
        for line in text.splitlines():
            p = next(csv.reader([line]))
            if len(p) >= 6 and p[2].strip().upper() == "MATCH":
                oid = p[0].strip().strip('"')
                coords = p[5].strip() if len(p) > 5 else ""
                if "," in coords:
                    try:
                        lng, lat = coords.split(",", 1)
                        results[oid] = (float(lat.strip()), float(lng.strip()))
                    except ValueError: pass
    except Exception as e:
        print(f"  Census error: {e}", flush=True)
    return results

def run():
    with psycopg.connect(DB, row_factory=dict_row) as c:
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lat DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lng DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS geocoded_at TIMESTAMPTZ")
        c.execute("CREATE INDEX IF NOT EXISTS ao_latlng ON account_offices (lat,lng) WHERE lat IS NOT NULL")
        c.commit()
        pending = c.execute("""
            SELECT id, address, city, state, zip FROM account_offices
            WHERE NOT deleted AND lat IS NULL AND geocoded_at IS NULL
              AND trim(coalesce(city,'')) != ''
            ORDER BY state, city
        """).fetchall()
    print(f"Pending: {len(pending)} offices", flush=True)
    total_ok = total_fail = 0
    for start in range(0, len(pending), BATCH):
        chunk = pending[start:start+BATCH]
        rows = [(r["id"],r["address"],r["city"],r["state"],r["zip"]) for r in chunk]
        print(f"Batch {start//BATCH+1}: {len(rows)} addresses...", flush=True)
        matches = census_batch(rows)
        print(f"  Matched: {len(matches)}/{len(rows)}", flush=True)
        with psycopg.connect(DB, row_factory=dict_row) as c:
            for r in chunk:
                oid = r["id"]
                if oid in matches:
                    lat, lng = matches[oid]
                    c.execute("UPDATE account_offices SET lat=%s,lng=%s,geocoded_at=now() WHERE id=%s",(lat,lng,oid))
                    total_ok += 1
                else:
                    c.execute("UPDATE account_offices SET geocoded_at=now() WHERE id=%s",(oid,))
                    total_fail += 1
            c.commit()
        print(f"  Total: {total_ok} geocoded, {total_fail} unmatched", flush=True)
        if start + BATCH < len(pending):
            time.sleep(2)
    with psycopg.connect(DB, row_factory=dict_row) as c:
        n = c.execute("SELECT count(*) FROM account_offices WHERE lat IS NOT NULL").fetchone()["count"]
    print(f"\nDone. {total_ok} geocoded, {total_fail} unmatched. Total with coords: {n}", flush=True)

if __name__ == "__main__":
    run()
