import psycopg, os, sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))

PAIRS = [
    ("WWM Operating, LLC. (Whitewater Midstream)", "WWM Operating, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Pelican Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Whistler Pipeline LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Delaware Basin Residue, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Bay Runner Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Bay Runner Pipeline Supply, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "White Water Midstream"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Matterhorn Express Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Blackcomb Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Blackfin Pipeline, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Waha Connector, LLC"),
    ("WWM Operating, LLC. (Whitewater Midstream)", "Agua Blanca, LLC"),
    ("TC Energy", "ANR PIPELINE COMPANY"),
    ("TC Energy", "COLUMBIA GAS TRANSMISSION, LLC"),
    ("TC Energy", "GREAT LAKES GAS TRANSMISSION LIMITED PARTNERSHIP"),
    ("TC Energy", "NORTHERN BORDER PIPELINE COMPANY"),
    ("TC Energy", "TC LOUISIANA INTRASTATE PIPELINE LLC"),
    ("Tallgrass Energy Partners, LP", "IRON HORSE PIPELINE, LLC"),
    ("Tallgrass Energy Partners, LP", "ROCKIES EXPRESSF PIPELINE, LLC"),
    ("Tallgrass Energy Partners, LP", "TALLGRASS INTERSTATE GAS"),
    ("Tallgrass Energy Partners, LP", "TALLGRASS TERMINALS, LLC"),
    ("Tallgrass Energy Partners, LP", "RUBY PIPELINE LLC"),
    ("The Williams Companies, Inc.", "APPALACHIA MIDSTREAM SERVICES"),
    ("The Williams Companies, Inc.", "BLUE RACER MIDSTREAM"),
    ("The Williams Companies, Inc.", "GULF STREAM NATURAL GAS SYSTEM, LLC"),
    ("The Williams Companies, Inc.", "NORTHWEST PIPELINE LLC"),
    ("The Williams Companies, Inc.", "TRANSCONTINENTAL GAS PIPE LINE CO."),
    ("The Williams Companies, Inc.", "UTICA EAST OHIO MIDSTREAM LLC"),
    ("The Williams Companies, Inc.", "WILLIAMS FIELD SERVICES"),
    ("The Williams Companies, Inc.", "WILLIAMS OHIO VALLEY MIDSTREAM"),
    ("Phillips 66", "DCP MIDSTREAM, LP"),
    ("Phillips 66", "DCP OPERATING COMPANY, LP"),
    ("Phillips 66", "PHILLIPS 66 PIPELINE LLC"),
    ("Phillips 66", "PIONEER PIPE LINE COMPANY"),
    ("Plains All American Pipeline (PAAPL)", "CACTUS II PIPELINE LLC"),
    ("Plains All American Pipeline (PAAPL)", "MDE MIDSTREAM, LLC"),
    ("Plains All American Pipeline (PAAPL)", "ORYX MIDLAND OIL GATHERING LLC"),
    ("Plains All American Pipeline (PAAPL)", "PLAINS ALL AMERICAN PIPELINE"),
    ("Plains All American Pipeline (PAAPL)", "PLAINS PIPELINE, L.P."),
    ("Plains All American Pipeline (PAAPL)", "PLAINS MARKETING, L.P."),
    ("Energy Transfer Operating", "ENERGY TRANSFER COMPANY"),
    ("Energy Transfer Operating", "ENERGY TRANSFER PARTNERS"),
    ("Energy Transfer Operating", "SUNOCO PIPELINE LP"),
    ("Energy Transfer Operating", "FLORIDA GAS TRANSMISSION"),
    ("Energy Transfer Operating", "Panhandle Eastern Pipeline"),
    ("Energy Transfer Operating", "CRESTWOOD MIDSTREAM PARTNERS"),
    ("Kinder Morgan Inc.", "COLORADO INTERSTATE GAS CO LLC"),
    ("Kinder Morgan Inc.", "EL PASO NATURAL GAS COMPANY"),
    ("Kinder Morgan Inc.", "KINDER MORGAN"),
    ("Kinder Morgan Inc.", "NATURAL GAS PIPELINE"),
    ("Kinder Morgan Inc.", "PERMIAN HIGHWAY PIPELINE, LLC"),
    ("Kinder Morgan Inc.", "SOUTHERN NATURAL GAS COMPANY"),
    ("Kinder Morgan Inc.", "TENNESSEE GAS PIPELINE"),
    ("Kinder Morgan Inc.", "WYOMING INTERSTATE COMPANY LLC"),
    ("ONEOK Inc.", "ONEOK ARBUCKLE II PIPELINE LLC"),
    ("ONEOK Inc.", "ONEOK BAKKEN PIPELINE LLC"),
    ("ONEOK Inc.", "ONEOK FIELD SERVICES"),
    ("ONEOK Inc.", "ONEOK GAS STORAGE LLC"),
    ("ONEOK Inc.", "ONEOK GAS TRANSPORTATION LLC"),
    ("ONEOK Inc.", "ONEOK NGL PIPELINE LLC"),
    ("ONEOK Inc.", "ONEOK INC"),
    ("ONEOK Inc.", "MAGELLAN PIPELINE COMPANY"),
    ("ONEOK Inc.", "WEST TEXAS LPG"),
    ("Enbridge Inc.", "ENBRIDGE (US) INC"),
    ("Enbridge Inc.", "ENBRIDGE ENERGY LIMITED PARTNERSHIP"),
    ("Enbridge Inc.", "TEXAS EASTERN TRANSMISSION"),
    ("Enbridge Inc.", "TEXAS GAS TRANSMISSION"),
    ("Enbridge Inc.", "THE EAST OHIO GAS COMPANY"),
    ("Enbridge Inc.", "QUESTAR GAS COMPANY"),
    ("Quanta Services LLC.", "Mears Group"),
    ("Quanta Services LLC.", "Price Gregory"),
    ("Quanta Services LLC.", "M.G. Dyess"),
    ("Quanta Services LLC.", "H.L. Chapman Pipeline Construction"),
    ("Quanta Services LLC.", "Irby Construction Company"),
    ("Quanta Services LLC.", "Under Ground Construction Company"),
    ("Quanta Services LLC.", "Underground Pipeline Services"),
    ("MasTec, Inc.", "Hanging H Companies"),
    ("MasTec, Inc.", "Precision Pipeline, LLC"),
    ("Primoris Services Corporation", "Primoris Energy Services"),
    ("Primoris Services Corporation", "Primoris Pipeline"),
    ("Primoris Services Corporation", "Rockford Corporation"),
]

def resolve(conn, name):
    norm = name.upper().strip().rstrip(".").rstrip(",").strip()
    rows = conn.execute(
        "SELECT id, name, types, sales_ytd FROM accounts"
        " WHERE upper(trim(name)) = %s"
        " ORDER BY length(coalesce(types,chr(32))) DESC, coalesce(sales_ytd,0) DESC",
        (norm,)
    ).fetchall()
    if not rows:
        short = norm
        for suffix in ["LLC", "INC", "LP", "LTD", "CORP"]:
            short = short.rstrip(suffix).strip().rstrip(",").strip()
        if len(short) > 6:
            rows = conn.execute(
                "SELECT id, name, types, sales_ytd FROM accounts"
                " WHERE upper(trim(name)) LIKE %s"
                " ORDER BY length(coalesce(types,chr(32))) DESC, coalesce(sales_ytd,0) DESC LIMIT 1",
                ("%" + short + "%",)
            ).fetchall()
    return rows[0] if rows else None

with psycopg.connect(os.environ["DATABASE_URL"], row_factory=psycopg.rows.dict_row) as conn:
    resolved_parents = {}
    for pname, _ in PAIRS:
        if pname not in resolved_parents:
            r = resolve(conn, pname)
            if r:
                resolved_parents[pname] = r
            else:
                print(f"UNRESOLVED PARENT: {pname!r}")

    plan = []
    seen = set()
    for pname, cname in PAIRS:
        prec = resolved_parents.get(pname)
        if not prec:
            continue
        crec = resolve(conn, cname)
        if not crec:
            print(f"UNRESOLVED CHILD: {cname!r}")
            continue
        if crec["id"] == prec["id"] or crec["id"] in seen:
            continue
        seen.add(crec["id"])
        plan.append((crec["id"], crec["name"], crec["types"], prec["id"], prec["name"]))

    print(f"\nParents resolved: {len(resolved_parents)}")
    print(f"Children to update: {len(plan)}")
    print("\n--- PREVIEW ---")
    for cid, cname, ctypes, pid, pname in plan:
        print(f"  {cname!r} ({ctypes}) -> {pname!r}")

    if "--apply" not in sys.argv:
        print(f"\nRun with --apply to write.")
        sys.exit(0)

    for cid, cname, ctypes, pid, pname in plan:
        conn.execute("UPDATE accounts SET parent_id=%s, root_id=%s WHERE id=%s", (pid, pid, cid))
    for prec in resolved_parents.values():
        conn.execute("UPDATE accounts SET root_id=%s WHERE id=%s AND root_id IS NULL", (prec["id"], prec["id"]))
    conn.commit()
    print(f"\nDone: {len(plan)} updated.")
