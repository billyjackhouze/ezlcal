"""ezlcal API -- served behind IIS at /api/*, bound to 127.0.0.1 only."""
import datetime as dt
import hashlib
import json
import os
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
            "SELECT username, staff_id, display_name, must_change, is_admin FROM app_users WHERE username=%s", (sub,)
        ).fetchone()
    if not u:
        raise HTTPException(401, "Account no longer exists")
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
            " || (SELECT count(*) FROM staff WHERE active)::text AS s"
        ).fetchone()["s"]
        etag = '"' + hashlib.sha1((stamp or "").encode()).hexdigest()[:16] + '"'
        if if_none_match == etag:
            return Response(status_code=304, headers={"ETag": etag})
        acc = c.execute(
            "SELECT id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order FROM accounts ORDER BY name"
        ).fetchall()
        con = c.execute("SELECT id,name,account_id FROM contacts ORDER BY name").fetchall()
        stf = c.execute("SELECT id,name,dept FROM staff WHERE active ORDER BY name").fetchall()
    response.headers["ETag"] = etag
    return {
        "accounts": [
            [a["id"], a["name"], a["types"], a["parent_id"], a["root_id"], float(a["sales_ytd"]),
             float(a["sales_py"]), float(a["quotes_ytd"]), a["last_order"].isoformat() if a["last_order"] else None]
            for a in acc
        ],
        "contacts": [[x["id"], x["name"], x["account_id"]] for x in con],
        "staff": [[s["id"], s["name"], s["dept"]] for s in stf],
    }


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
        # last write wins, by the time the edit was made on the device
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
