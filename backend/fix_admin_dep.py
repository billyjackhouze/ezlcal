from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")
old = "def set_user_prefs(username: str, body: dict, u: dict = Depends(admin_user)):"
new = "def set_user_prefs(username: str, body: dict, u: dict = Depends(current_user)):\n    if not u.get('is_admin'): raise HTTPException(403, 'Admin only')"
assert old in src
src = src.replace(old, new, 1)
f.write_text(src, encoding="utf-8")
print("OK")
