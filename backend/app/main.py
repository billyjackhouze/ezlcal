"""ezlcal API -- served behind IIS at /api/*, bound to 127.0.0.1 only."""
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import string
from pathlib import Path

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Response
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET = os.environ["JWT_SECRET"]
TOKEN_DAYS = int(os.environ.get("TOKEN_DAYS", "30"))

pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=8, kwargs={"row_factory": dict_row}, open=True)
app = FastAPI(title="ezlcal", docs_url=None, redoc_url=None, openapi_url=None)


# ---------- auth ----------
def make_token(username: str) -> str:
    exp = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=TOKEN_DAYS)
    return jwt.encode({"sub": username, "exp": exp}, JWT_SECRET, algorithm="HS256")


def current_user(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Sign in required")
    try:
        sub = jwt.decode(authorization[7:], JWT_SECRET, algorithms=["HS256"])["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Session expired, sign in again")
    with pool.connection() as c:
        u = c.execute(
            "SELECT username, staff_id, display_name, must_change, is_admin, disabled FROM app_users WHERE username=%s", (sub,)
        ).fetchone()
    if not u or u["disabled"]:
        raise HTTPException(401, "This account is not active")
    return u


class LoginIn(BaseModel):
    username: str
    password: str


class PasswordIn(BaseModel):
    current: str
    new: str = Field(min_length=8)


@app.get("/api/health")
def health():
    with pool.connection() as c:
        c.execute("SELECT 1")
    return {"ok": True}


@app.post("/api/login")
def login(body: LoginIn):
    with pool.connection() as c:
        u = c.execute("SELECT * FROM app_users WHERE lower(username)=lower(%s)", (body.username.strip(),)).fetchone()
    if not u or not bcrypt.checkpw(body.password.encode(), u["pw_hash"].encode()):
        raise HTTPException(401, "That username and password don't match")
    if u["disabled"]:
        raise HTTPException(401, "This account has been turned off. Ask your administrator.")
    with pool.connection() as c:
        c.execute("UPDATE app_users SET last_login=now() WHERE username=%s", (u["username"],))
    return {"token": make_token(u["username"]), "user": _public(u)}


@app.get("/api/me")
def me(u: dict = Depends(current_user)):
    return _public(u)


@app.post("/api/password")
def change_password(body: PasswordIn, u: dict = Depends(current_user)):
    with pool.connection() as c:
        row = c.execute("SELECT pw_hash FROM app_users WHERE username=%s", (u["username"],)).fetchone()
        if not bcrypt.checkpw(body.current.encode(), row["pw_hash"].encode()):
            raise HTTPException(400, "Current password is wrong")
        h = bcrypt.hashpw(body.new.encode(), bcrypt.gensalt()).decode()
        c.execute("UPDATE app_users SET pw_hash=%s, must_change=false WHERE username=%s", (h, u["username"]))
    return {"ok": True}


def _public(u: dict) -> dict:
    return {k: u[k] for k in ("username", "staff_id", "display_name", "must_change", "is_admin")}


# ---------- reference data ----------
@app.get("/api/bootstrap")
def bootstrap(response: Response, if_none_match: str = Header(default=""), u: dict = Depends(current_user)):
    with pool.connection() as c:
        stamp = c.execute(
            "SELECT (SELECT max(updated_at) FROM accounts)::text || (SELECT max(updated_at) FROM contacts)::text"
            " || (SELECT count(*) FROM staff WHERE active)::text || (SELECT count(*) FROM contact_accounts)::text"
            " || coalesce((SELECT max(updated_at) FROM account_offices)::text,'') || 'v3' AS s"
        ).fetchone()["s"]
        etag = '"' + hashlib.sha1((stamp or "").encode()).hexdigest()[:16] + '"'
        if if_none_match == etag:
            return Response(status_code=304, headers={"ETag": etag})
        acc = c.execute(
            "SELECT id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order,address,city,state,zip,homepage"
            " FROM accounts ORDER BY name"
        ).fetchall()
        con = c.execute(
            "SELECT id,name,account_id,title,email,phone_direct,phone_mobile,address,city,state,zip,linkedin,work_remote,active"
            " FROM contacts ORDER BY name"
        ).fetchall()
        stf = c.execute("SELECT id,name,dept FROM staff WHERE active ORDER BY name").fetchall()
        lnk = c.execute("SELECT contact_id,account_id,sales_ytd,sales_py,quotes_ytd FROM contact_accounts").fetchall()
        off = c.execute(
            "SELECT id,account_id,office_type,address,city,state,zip,phone,email,notes,source FROM account_offices"
            " WHERE NOT deleted ORDER BY office_type, city"
        ).fetchall()
    response.headers["ETag"] = etag
    return {
        "accounts": [
            [a["id"], a["name"], a["types"], a["parent_id"], a["root_id"], float(a["sales_ytd"]),
             float(a["sales_py"]), float(a["quotes_ytd"]), a["last_order"].isoformat() if a["last_order"] else None,
             a["address"], a["city"], a["state"], a["zip"], a["homepage"]]
            for a in acc
        ],
        "contacts": [[x["id"], x["name"], x["account_id"], x["title"], x["email"], x["phone_direct"], x["phone_mobile"],
                      x["address"], x["city"], x["state"], x["zip"], x["linkedin"], x["work_remote"], x["active"]] for x in con],
        "staff": [[s["id"], s["name"], s["dept"]] for s in stf],
        "links": [[l["contact_id"], l["account_id"], float(l["sales_ytd"]), float(l["sales_py"]), float(l["quotes_ytd"])] for l in lnk],
        "offices": [[o["id"], o["account_id"], o["office_type"], o["address"], o["city"], o["state"], o["zip"], o["phone"],
                     o["email"], o["notes"], o["source"]] for o in off],
    }


# ---------- offices ----------
class OfficeIn(BaseModel):
    account_id: str
    office_type: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    phone: str = ""
    email: str = ""
    notes: str = ""


@app.put("/api/offices/{office_id}")
def put_office(office_id: str, o: OfficeIn, u: dict = Depends(current_user)):
    vals = [o.office_type.strip()[:60], o.address.strip()[:300], o.city.strip()[:120], o.state.strip()[:40],
            o.zip.strip()[:20], o.phone.strip()[:60], o.email.strip()[:200], o.notes.strip()[:2000]]
    if not any(vals[1:7]):
        raise HTTPException(400, "Add at least an address, city, phone or email")
    with pool.connection() as c, c.transaction():
        if not c.execute("SELECT 1 FROM accounts WHERE id=%s", (o.account_id,)).fetchone():
            raise HTTPException(400, "Unknown account")
        c.execute(
            """INSERT INTO account_offices (id,account_id,office_type,address,city,state,zip,phone,email,notes,source,updated_by,updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'web',%s,now())
               ON CONFLICT (id) DO UPDATE SET office_type=EXCLUDED.office_type,address=EXCLUDED.address,city=EXCLUDED.city,
                 state=EXCLUDED.state,zip=EXCLUDED.zip,phone=EXCLUDED.phone,email=EXCLUDED.email,notes=EXCLUDED.notes,
                 source='web',deleted=false,updated_by=EXCLUDED.updated_by,updated_at=now()""",
            (office_id, o.account_id, *vals, u["username"]),
        )
    return {"ok": True, "office": [office_id, o.account_id, *vals, "web"]}


@app.delete("/api/offices/{office_id}")
def delete_office(office_id: str, u: dict = Depends(current_user)):
    with pool.connection() as c:
        n = c.execute("UPDATE account_offices SET deleted=true, source='web', updated_by=%s, updated_at=now() WHERE id=%s",
                      (u["username"], office_id)).rowcount
    if not n:
        raise HTTPException(404, "No such office")
    return {"ok": True}


# ---------- account creation ----------
class AccountIn(BaseModel):
    name: str
    types: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    homepage: str = ""


@app.post("/api/accounts")
def create_account(body: AccountIn, u: dict = Depends(current_user)):
    import uuid as _uuid
    name = body.name.strip()[:300]
    if not name:
        raise HTTPException(400, "Account name is required")
    types = "".join(c for c in body.types if c in "CUG")[:10]
    acct_id = str(_uuid.uuid4())
    with pool.connection() as c, c.transaction():
        c.execute(
            """INSERT INTO accounts (id,name,types,address,city,state,zip,homepage,
               sales_ytd,sales_py,quotes_ytd,updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,0,0,now())""",
            (acct_id, name, types, body.address.strip()[:300], body.city.strip()[:120],
             body.state.strip()[:40], body.zip.strip()[:20], body.homepage.strip()[:300]),
        )
    return {"ok": True, "account": [acct_id, name, types, None, None, 0.0, 0.0, 0.0, None,
                                     body.address.strip(), body.city.strip(),
                                     body.state.strip(), body.zip.strip(), body.homepage.strip()]}


# ---------- contact creation ----------
class ContactIn(BaseModel):
    name_first: str
    name_last: str = ""
    account_id: str | None = None
    title: str = ""
    email: str = ""
    phone_direct: str = ""
    phone_mobile: str = ""


@app.post("/api/contacts")
def create_contact(body: ContactIn, u: dict = Depends(current_user)):
    import time as _time
    first = body.name_first.strip()[:200]
    last = body.name_last.strip()[:200]
    full = (first + " " + last).strip()
    if not full:
        raise HTTPException(400, "Contact name is required")
    contact_id = "W" + str(int(_time.time() * 1000))[-9:]
    with pool.connection() as c, c.transaction():
        if body.account_id:
            if not c.execute("SELECT 1 FROM accounts WHERE id=%s", (body.account_id,)).fetchone():
                raise HTTPException(400, "Unknown account")
        c.execute(
            """INSERT INTO contacts (id,name,account_id,title,email,phone_direct,phone_mobile,
               work_remote,active,updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,false,true,now())""",
            (contact_id, full, body.account_id or None, body.title.strip()[:200],
             body.email.strip()[:300], body.phone_direct.strip()[:60], body.phone_mobile.strip()[:60]),
        )
        if body.account_id:
            c.execute(
                """INSERT INTO contact_accounts (contact_id,account_id,sales_ytd,sales_py,quotes_ytd)
                   VALUES (%s,%s,0,0,0) ON CONFLICT DO NOTHING""",
                (contact_id, body.account_id),
            )
    return {"ok": True, "contact": [contact_id, full, body.account_id, body.title.strip(),
                                     body.email.strip(), body.phone_direct.strip(),
                                     body.phone_mobile.strip(), "", "", "", "", "", False, True]}


# ---------- events ----------
class EventIn(BaseModel):
    id: str
    title: str
    date: str
    time: str = ""
    end: str = ""
    cat: str = ""
    loc: str = ""
    notes: str = ""
    att: list[list[str]] = []
    deleted: bool = False
    updatedAt: str | None = None


def _event_rows(c, where: str = "", params: tuple = ()) -> list[dict]:
    evs = c.execute(
        "SELECT id,title,date,start_time,end_time,category,location,notes,deleted,updated_at,updated_by "
        f"FROM events {where} ORDER BY updated_at", params
    ).fetchall()
    if not evs:
        return []
    ids = [e["id"] for e in evs]
    att: dict[str, list] = {}
    for r in c.execute("SELECT event_id, attendee_type, ref_id FROM event_attendees WHERE event_id = ANY(%s)", (ids,)):
        att.setdefault(r["event_id"], []).append([r["attendee_type"].strip(), r["ref_id"]])
    return [
        {"id": e["id"], "title": e["title"], "date": e["date"].isoformat(), "time": e["start_time"],
         "end": e["end_time"], "cat": e["category"], "loc": e["location"], "notes": e["notes"],
         "deleted": e["deleted"], "att": att.get(e["id"], []),
         "updatedAt": e["updated_at"].isoformat(), "updatedBy": e["updated_by"]}
        for e in evs
    ]


@app.get("/api/events")
def list_events(since: str | None = None, u: dict = Depends(current_user)):
    with pool.connection() as c:
        if since:
            rows = _event_rows(c, "WHERE updated_at > %s", (since,))
        else:
            rows = _event_rows(c, "WHERE NOT deleted")
        now = c.execute("SELECT now()::text AS n").fetchone()["n"]
    return {"events": rows, "serverTime": now}


@app.put("/api/events/{event_id}")
def put_event(event_id: str, ev: EventIn, u: dict = Depends(current_user)):
    if ev.id != event_id:
        raise HTTPException(400, "Event id mismatch")
    try:
        day = dt.date.fromisoformat(ev.date)
    except ValueError:
        raise HTTPException(400, "Bad date")
    att = {(t, str(r)) for t, r in ev.att if t in ("s", "a", "c")}
    if len(att) > 150:
        raise HTTPException(400, "Too many invitees (150 max)")
    with pool.connection() as c, c.transaction():
        cur = c.execute("SELECT updated_at FROM events WHERE id=%s FOR UPDATE", (event_id,)).fetchone()
        incoming = dt.datetime.fromisoformat(ev.updatedAt.replace("Z", "+00:00")) if ev.updatedAt else None
        if cur and incoming and incoming < cur["updated_at"]:
            return {"ok": True, "stale": True, "event": _event_rows(c, "WHERE id=%s", (event_id,))[0]}
        c.execute(
            """INSERT INTO events (id,title,date,start_time,end_time,category,location,notes,deleted,created_by,updated_by,updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
               ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title,date=EXCLUDED.date,start_time=EXCLUDED.start_time,
                 end_time=EXCLUDED.end_time,category=EXCLUDED.category,location=EXCLUDED.location,notes=EXCLUDED.notes,
                 deleted=EXCLUDED.deleted,updated_by=EXCLUDED.updated_by,updated_at=now()""",
            (event_id, ev.title.strip()[:300], day, ev.time[:5], ev.end[:5], ev.cat[:60], ev.loc[:300], ev.notes[:20000],
             ev.deleted, u["username"], u["username"]),
        )
        c.execute("DELETE FROM event_attendees WHERE event_id=%s", (event_id,))
        if att:
            with c.cursor() as cur2:
                cur2.executemany(
                    "INSERT INTO event_attendees (event_id,attendee_type,ref_id) VALUES (%s,%s,%s)",
                    [(event_id, t, r) for t, r in att],
                )
        row = _event_rows(c, "WHERE id=%s", (event_id,))[0]
    return {"ok": True, "event": row}


# ---------- admin ----------
USERNAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,39}$")


def admin_user(u: dict = Depends(current_user)) -> dict:
    if not u["is_admin"]:
        raise HTTPException(403, "Administrators only")
    return u


def _temp_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "-".join("".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(3))


def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


class UserCreate(BaseModel):
    username: str
    display_name: str
    staff_id: str | None = None
    new_staff_dept: str | None = None
    is_admin: bool = False


class UserPatch(BaseModel):
    display_name: str | None = None
    staff_id: str | None = None
    unlink_staff: bool = False
    is_admin: bool | None = None
    disabled: bool | None = None


@app.get("/api/admin/users")
def admin_list(u: dict = Depends(admin_user)):
    with pool.connection() as c:
        users = c.execute(
            """SELECT a.username, a.display_name, a.staff_id, s.name AS staff_name, a.is_admin, a.disabled,
                      a.must_change, a.created_at, a.last_login, a.created_by
               FROM app_users a LEFT JOIN staff s ON s.id = a.staff_id ORDER BY a.display_name"""
        ).fetchall()
        staff = c.execute("SELECT id, name, dept, active FROM staff ORDER BY name").fetchall()
    for x in users:
        for k in ("created_at", "last_login"):
            x[k] = x[k].isoformat() if x[k] else None
    return {"users": users, "staff": staff, "me": u["username"]}


@app.post("/api/admin/users")
def admin_create(body: UserCreate, u: dict = Depends(admin_user)):
    username = body.username.strip().lower()
    name = body.display_name.strip()
    if not USERNAME_RE.match(username):
        raise HTTPException(400, "Username: 3-40 characters, lowercase letters, numbers, dot, dash or underscore")
    if not name:
        raise HTTPException(400, "Enter the person's name")
    pw = _temp_password()
    with pool.connection() as c, c.transaction():
        if c.execute("SELECT 1 FROM app_users WHERE lower(username)=%s", (username,)).fetchone():
            raise HTTPException(400, f"{username} already exists")
        staff_id = body.staff_id or None
        if staff_id:
            if not c.execute("SELECT 1 FROM staff WHERE id=%s", (staff_id,)).fetchone():
                raise HTTPException(400, "That staff member doesn't exist")
            if c.execute("SELECT 1 FROM app_users WHERE staff_id=%s", (staff_id,)).fetchone():
                raise HTTPException(400, "That staff member already has a login")
        elif body.new_staff_dept is not None:
            staff_id = "W" + secrets.token_hex(3).upper()
            c.execute("INSERT INTO staff (id,name,dept,active) VALUES (%s,%s,%s,true)",
                      (staff_id, name, body.new_staff_dept.strip()[:60]))
        c.execute(
            """INSERT INTO app_users (username,staff_id,display_name,pw_hash,must_change,is_admin,created_by)
               VALUES (%s,%s,%s,%s,true,%s,%s)""",
            (username, staff_id, name, _hash(pw), body.is_admin, u["username"]),
        )
    return {"username": username, "temp_password": pw}


@app.post("/api/admin/users/{username}/reset")
def admin_reset(username: str, u: dict = Depends(admin_user)):
    pw = _temp_password()
    with pool.connection() as c:
        n = c.execute("UPDATE app_users SET pw_hash=%s, must_change=true WHERE username=%s",
                      (_hash(pw), username)).rowcount
    if not n:
        raise HTTPException(404, "No such user")
    return {"username": username, "temp_password": pw}


@app.patch("/api/admin/users/{username}")
def admin_patch(username: str, body: UserPatch, u: dict = Depends(admin_user)):
    if username == u["username"] and (body.disabled or body.is_admin is False):
        raise HTTPException(400, "You can't turn off or remove admin from your own account")
    sets, vals = [], []
    if body.display_name is not None and body.display_name.strip():
        sets.append("display_name=%s"); vals.append(body.display_name.strip())
    if body.is_admin is not None:
        sets.append("is_admin=%s"); vals.append(body.is_admin)
    if body.disabled is not None:
        sets.append("disabled=%s"); vals.append(body.disabled)
    with pool.connection() as c, c.transaction():
        if body.unlink_staff:
            sets.append("staff_id=NULL")
        elif body.staff_id:
            if not c.execute("SELECT 1 FROM staff WHERE id=%s", (body.staff_id,)).fetchone():
                raise HTTPException(400, "That staff member doesn't exist")
            if c.execute("SELECT 1 FROM app_users WHERE staff_id=%s AND username<>%s", (body.staff_id, username)).fetchone():
                raise HTTPException(400, "That staff member already has a login")
            sets.append("staff_id=%s"); vals.append(body.staff_id)
        if not sets:
            return {"ok": True}
        n = c.execute(f"UPDATE app_users SET {', '.join(sets)} WHERE username=%s", (*vals, username)).rowcount
        if not n:
            raise HTTPException(404, "No such user")
    return {"ok": True}
