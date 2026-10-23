import psycopg, os, sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as c:
    dups = c.execute(
        "SELECT name, count(*) as cnt FROM accounts"
        " GROUP BY name HAVING count(*) > 1 ORDER BY cnt DESC"
    ).fetchall()
    print(f"Duplicate name groups: {len(dups)}")
    to_delete = []
    for row in dups:
        name = row["name"]
        candidates = c.execute(
            "SELECT id, name, types, sales_ytd FROM accounts WHERE name = %s"
            " ORDER BY length(coalesce(types,chr(32))) DESC, coalesce(sales_ytd,0) DESC",
            (name,)
        ).fetchall()
        keep = candidates[0]
        for drop in candidates[1:]:
            to_delete.append((drop["id"], drop["name"], drop["types"], keep["id"], keep["name"]))
    print(f"Accounts to delete: {len(to_delete)}")
    if "--apply" not in sys.argv:
        print("\nRun with --apply to delete.")
        sys.exit(0)
    deleted = 0
    for did, dname, dtypes, kid, kname in to_delete:
        # contact_accounts: if link to keeper already exists, delete the duplicate link
        # otherwise re-point it
        links = c.execute(
            "SELECT contact_id FROM contact_accounts WHERE account_id=%s", (did,)
        ).fetchall()
        for lnk in links:
            cid = lnk["contact_id"]
            exists = c.execute(
                "SELECT 1 FROM contact_accounts WHERE contact_id=%s AND account_id=%s",
                (cid, kid)
            ).fetchone()
            if exists:
                c.execute("DELETE FROM contact_accounts WHERE contact_id=%s AND account_id=%s", (cid, did))
            else:
                c.execute("UPDATE contact_accounts SET account_id=%s WHERE contact_id=%s AND account_id=%s", (kid, cid, did))
        c.execute("UPDATE account_quotes SET account_id=%s WHERE account_id=%s", (kid, did))
        c.execute("UPDATE account_offices SET account_id=%s WHERE account_id=%s", (kid, did))
        c.execute("UPDATE accounts SET parent_id=%s WHERE parent_id=%s", (kid, did))
        c.execute("UPDATE accounts SET root_id=%s WHERE root_id=%s", (kid, did))
        c.execute("DELETE FROM accounts WHERE id=%s", (did,))
        deleted += 1
    c.commit()
    after = c.execute("SELECT count(*) FROM accounts").fetchone()["count"]
    print(f"Done. Deleted {deleted}, accounts now: {after}")
