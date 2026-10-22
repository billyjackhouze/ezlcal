import psycopg, os, sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

# Manual parent name -> exact DB name mappings for unresolved parents
PARENT_OVERRIDES = {
    "WWM Operating, LLC. (Whitewater Midstream)": "White Water Midstream",
    "Energy Transfer Operating": "ENERGY TRANSFER",
    "MasTec, Inc.": "MASTEC NORTH AMERICA",
}

# Additional pairs not in the previous run (unresolved parents now fixed)
EXTRA_PAIRS = [
    ("WWM Operating, LLC. (Whitewater Midstream)", "WWM Operating, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Pelican Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Whistler Pipeline LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Delaware Basin Residue, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Bay Runner Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Bay Runner Pipeline Supply, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Matterhorn Express Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Blackcomb Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Blackfin Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Waha Connector, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Agua Blanca, LLC"),
    ("Energy Transfer Operating", "ENERGY TRANSFER COMPANY"),
    ("Energy Transfer Operating", "ENERGY TRANSFER PARTNERS"),
    ("Energy Transfer Operating", "SUNOCO PIPELINE LP"),
    ("Energy Transfer Operating", "FLORIDA GAS TRANSMISSION"),
    ("Energy Transfer Operating", "Panhandle Eastern Pipeline"),
    ("Energy Transfer Operating", "CRESTWOOD MIDSTREAM PARTNERS"),
    ("MasTec, Inc.", "Hanging H Companies"),
    ("MasTec, Inc.", "Precision Pipeline, LLC"),
]

def resolve_exact(conn, name):
    rows = conn.execute(
        "SELECT id, name, types FROM accounts WHERE upper(trim(name)) = %s"
        " ORDER BY length(coalesce(types,chr(32))) DESC, coalesce(sales_ytd,0) DESC",
        (name.upper().strip(),)
    ).fetchall()
    if not rows:
        rows = conn.execute(
            "SELECT id, name, types FROM accounts WHERE name ILIKE %s"
            " ORDER BY length(coalesce(types,chr(32))) DESC LIMIT 1",
            (name,)
        ).fetchall()
    return rows[0] if rows else None

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as conn:
    plan = []
    seen = set()

    for pname, cname in EXTRA_PAIRS:
        # Resolve parent using override name
        db_pname = PARENT_OVERRIDES.get(pname, pname)
        prec = resolve_exact(conn, db_pname)
        if not prec:
            print(f"STILL UNRESOLVED PARENT: {pname!r} (tried {db_pname!r})")
            continue
        crec = resolve_exact(conn, cname)
        if not crec:
            print(f"UNRESOLVED CHILD: {cname!r}")
            continue
        if crec["id"] == prec["id"] or crec["id"] in seen:
            continue
        seen.add(crec["id"])
        plan.append((crec["id"], crec["name"], crec["types"], prec["id"], prec["name"]))

    print(f"Additional children to update: {len(plan)}")
    for cid, cname, ctypes, pid, pname in plan:
        print(f"  {cname!r} ({ctypes}) -> {pname!r}")

    if "--apply" not in sys.argv:
        print("\nRun with --apply to write.")
        sys.exit(0)

    for cid, cname, ctypes, pid, pname in plan:
        conn.execute(
            "UPDATE accounts SET parent_id=%s, root_id=%s WHERE id=%s",
            (pid, pid, cid)
        )

    # Also fix White Water Midstream (CU) as its own root
    wwm = resolve_exact(conn, "White Water Midstream")
    if wwm:
        conn.execute(
            "UPDATE accounts SET root_id=%s WHERE id=%s AND root_id IS NULL",
            (wwm["id"], wwm["id"])
        )
    conn.commit()
    print(f"\nDone: {len(plan)} additional rows updated.")
