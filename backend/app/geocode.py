"""Geocode account_offices rows that have an address but no lat/lng.

Uses Nominatim (OpenStreetMap) — free, no API key, 1 req/sec limit.

  python -m app.geocode          geocode all un-geocoded offices
  python -m app.geocode --reset  clear all lat/lng and re-geocode
"""
import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

UA = "ezlcal/1.0 (ezlcal.alamark.com)"
DB = os.environ["DATABASE_URL"]


def geocode_one(address, city, state, zip_):
    parts = [p for p in [address, city, state, zip_, "USA"] if p and p.strip()]
    q = ", ".join(parts)
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": q, "format": "json", "limit": 1, "countrycodes": "us"
    })
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            results = json.loads(r.read())
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"  geocode error for '{q}': {e}")
    return None


def run(reset=False):
    with psycopg.connect(DB, row_factory=dict_row) as c:
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lat DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lng DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS geocoded_at TIMESTAMPTZ")
        c.execute("CREATE INDEX IF NOT EXISTS account_offices_latlng ON account_offices (lat, lng) WHERE lat IS NOT NULL")
        c.commit()
        if reset:
            c.execute("UPDATE account_offices SET lat=NULL, lng=NULL, geocoded_at=NULL")
            c.commit()
            print("Reset all geocodes.")
        rows = c.execute("""
            SELECT id, address, city, state, zip
            FROM account_offices
            WHERE NOT deleted
              AND (address != '' OR city != '')
              AND lat IS NULL
            ORDER BY id
        """).fetchall()

    print(f"Found {len(rows)} offices to geocode.")
    ok = fail = skip = 0

    for row in rows:
        oid = row["id"]
        addr, city, state, zip_ = row["address"], row["city"], row["state"], row["zip"]
        if not (addr or city):
            skip += 1
            continue
        result = geocode_one(addr, city, state, zip_)
        with psycopg.connect(DB, row_factory=dict_row) as c:
            if result:
                lat, lng = result
                c.execute("UPDATE account_offices SET lat=%s, lng=%s, geocoded_at=now() WHERE id=%s", (lat, lng, oid))
                print(f"  OK  {city}, {state} -> {lat:.4f}, {lng:.4f}  [{addr[:40]}]")
                ok += 1
            else:
                c.execute("UPDATE account_offices SET geocoded_at=now() WHERE id=%s", (oid,))
                print(f"  --  no result for: {addr}, {city}, {state}")
                fail += 1
            c.commit()
        time.sleep(1.1)

    print(f"\nDone: {ok} geocoded, {fail} failed, {skip} skipped.")


if __name__ == "__main__":
    run(reset="--reset" in sys.argv)
