import os, sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
sys.path.insert(0, r"C:\Apps\ezlcal\backend")
from app.fmsync import _cfg, _login
host, db, user, pw = _cfg(live=True)
print("host:", repr(host))
print("db:", repr(db))
print("user:", repr(user))
print("pw:", repr(pw))
print("Trying login...")
try:
    token = _login(host, db, user, pw)
    print("SUCCESS:", token[:20])
except Exception as e:
    print("FAILED:", e)
