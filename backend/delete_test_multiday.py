import psycopg, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"]) as c:
    ids = [
        "9746849b-6349-4786-a1f3-734aeb4a8ee0",
        "a95d8156-f3f9-4aaa-94ac-729ee60dbb2c",
        "a7dd5a27-ba7e-42ea-8083-62aa614e4b93",
        "4656c9df-6aff-47fe-bd31-5335c1673df9",
    ]
    for id in ids:
        c.execute("UPDATE events SET deleted=TRUE WHERE id=%s", (id,))
        print("Deleted:", id)
    c.commit()
    print("Done")
