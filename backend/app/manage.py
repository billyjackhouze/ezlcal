"""ezlcal management commands.

  python -m app.manage migrate              create/upgrade tables (safe to re-run)
  python -m app.manage seed                 load seed/seed.json (reference data upserts; events only if missing)
  python -m app.manage create-users         one login per staff member; prints temp passwords ONCE
  python -m app.manage reset-password USER  new temp password for one user
"""
import json
import secrets
import string
import sys
from pathlib import Path

import bcrypt
import psycopg
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def conn():
    return psycopg.connect(os.environ["DATABASE_URL"])


def temp_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "-".join("".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(3))


def migrate():
    sql = (ROOT / "app" / "schema.sql").read_text(encoding="utf-8")
    with conn() as c:
        c.execute(sql)
    print("Schema is up to date.")


def seed():
    data = json.loads((ROOT / "seed" / "seed.json").read_text(encoding="utf-8"))
    with conn() as c, c.cursor() as cur:
        cur.executemany(
            """INSERT INTO accounts (id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order,updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
               ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,types=EXCLUDED.types,parent_id=EXCLUDED.parent_id,
                 root_id=EXCLUDED.root_id,sales_ytd=EXCLUDED.sales_ytd,sales_py=EXCLUDED.sales_py,
                 quotes_ytd=EXCLUDED.quotes_ytd,last_order=EXCLUDED.last_order,updated_at=now()""",
            [tuple(a) for a in data["accounts"]],
        )
        cur.executemany(
            """INSERT INTO contacts (id,name,account_id,updated_at) VALUES (%s,%s,%s,now())
               ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,account_id=EXCLUDED.account_id,updated_at=now()""",
            [tuple(x) for x in data["contacts"]],
        )
        cur.executemany(
            """INSERT INTO staff (id,name,dept) VALUES (%s,%s,%s)
               ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,dept=EXCLUDED.dept""",
            [tuple(s) for s in data["staff"]],
        )
        added = 0
        for e in data["events"]:
            cur.execute(
                """INSERT INTO events (id,title,date,start_time,end_time,category,location,notes,legacy_fm_id,created_by,updated_by)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'migration','migration') ON CONFLICT (id) DO NOTHING""",
                (e["id"], e["title"], e["date"], e["time"], e["end"], e["cat"], e["loc"], e["notes"], e["id"]),
            )
            if cur.rowcount:
                added += 1
                cur.executemany(
                    "INSERT INTO event_attendees (event_id,attendee_type,ref_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    [(e["id"], t, r) for t, r in e["att"]],
                )
    print(f"Seeded {len(data['accounts'])} accounts, {len(data['contacts'])} contacts, "
          f"{len(data['staff'])} staff, {added} new events (existing events left untouched).")


def create_users():
    made = []
    with conn() as c:
        staff = c.execute("SELECT id,name FROM staff WHERE active ORDER BY name").fetchall()
        for sid, name in staff:
            if c.execute("SELECT 1 FROM app_users WHERE staff_id=%s", (sid,)).fetchone():
                continue
            parts = name.lower().split()
            username = (parts[0] + "." + parts[-1]) if len(parts) > 1 else parts[0]
            pw = temp_password()
            c.execute(
                "INSERT INTO app_users (username,staff_id,display_name,pw_hash,is_admin) VALUES (%s,%s,%s,%s,%s)",
                (username, sid, name, bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode(), name == "Trey Palmer"),
            )
            made.append((name, username, pw))
    if not made:
        print("Every active staff member already has a login.")
        return
    print("\nNew logins (temporary passwords; each person sets their own at first sign-in).")
    print("These are shown ONCE. Hand them out, then clear this window.\n")
    for name, username, pw in made:
        print(f"  {name:<20} {username:<22} {pw}")


def reset_password(username: str):
    pw = temp_password()
    with conn() as c:
        n = c.execute(
            "UPDATE app_users SET pw_hash=%s, must_change=true WHERE lower(username)=lower(%s)",
            (bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode(), username),
        ).rowcount
    print(f"Temporary password for {username}: {pw}" if n else f"No user named {username}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "migrate":
        migrate()
    elif cmd == "seed":
        seed()
    elif cmd == "create-users":
        create_users()
    elif cmd == "reset-password" and len(sys.argv) > 2:
        reset_password(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
