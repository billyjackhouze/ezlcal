import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
UA = "ezlcal/1.0 (ezlcal.alamark.com)"
DB = os.environ["DATABASE_URL"]
SLEEP = 2.0  # stay well under 1 req/sec

def geocode_q(q):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "limit": 1, "countrycodes": "us"}
    )
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=10) as r:
                results = json.loads(r.read())
            if results:
                return float(results[0]["lat"]), float(results[0]["lon"])
            return None
        except Exception as e:
            if "429" in str(e):
                wait = 10 * (attempt + 1)
                print(f"  429 rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"  error: {e}", flush=True)
                return None
    return None

def run(city_only=False):
    with psycopg.connect(DB, row_factory=dict_row) as c:
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lat DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS lng DOUBLE PRECISION")
        c.execute("ALTER TABLE account_offices ADD COLUMN IF NOT EXISTS geocoded_at TIMESTAMPTZ")
        c.execute("CREATE INDEX IF NOT EXISTS ao_latlng ON account_offices (lat,lng) WHERE lat IS NOT NULL")
        c.commit()
        combos = c.execute("""
            SELECT DISTINCT trim(city) as city, trim(state) as state
            FROM account_offices
            WHERE NOT deleted AND lat IS NULL
              AND trim(city) != '' AND trim(state) != ''
              AND trim(city) NOT LIKE '%|%'
              AND trim(city) NOT LIKE '%''%'
              AND trim(city) NOT LIKE '%,%'
              AND length(trim(state)) <= 3
            ORDER BY state, city
        """).fetchall()

    print(f"Unique city/state combos to geocode: {len(combos)}", flush=True)
    cache = {}
    ok = fail = 0

    for i, row in enumerate(combos):
        city, state = row["city"], row["state"]
        key = (city.upper(), state.upper())
        if key in cache:
            continue
        q = f"{city}, {state}, USA"
        result = geocode_q(q)
        cache[key] = result
        if result:
            lat, lng = result
            print(f"  OK  {city}, {state} -> {lat:.4f}, {lng:.4f}  [{i+1}/{len(combos)}]", flush=True)
            ok += 1
        else:
            print(f"  --  {city}, {state}  [{i+1}/{len(combos)}]", flush=True)
            fail += 1
        time.sleep(SLEEP)

    print(f"\nGeocoded {ok}/{ok+fail} combos. Backfilling...", flush=True)
    with psycopg.connect(DB, row_factory=dict_row) as c:
        rows = c.execute("""
            SELECT id, trim(city) as city, trim(state) as state
            FROM account_offices WHERE NOT deleted AND lat IS NULL
        """).fetchall()
        updated = 0
        for row in rows:
            key = (row["city"].upper(), row["state"].upper())
            result = cache.get(key)
            if result:
                lat, lng = result
                c.execute("UPDATE account_offices SET lat=%s, lng=%s, geocoded_at=now() WHERE id=%s",
                          (lat, lng, row["id"]))
                updated += 1
            else:
                c.execute("UPDATE account_offices SET geocoded_at=now() WHERE id=%s", (row["id"],))
        c.commit()
        geocoded = c.execute("SELECT count(*) FROM account_offices WHERE lat IS NOT NULL").fetchone()["count"]
        print(f"Updated {updated} offices. Total geocoded: {geocoded}", flush=True)

if __name__ == "__main__":
    run(city_only="--city" in sys.argv)

