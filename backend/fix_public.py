from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")
old = 'return {k: u[k] for k in ("username", "staff_id", "display_name", "must_change", "is_admin", "default_tab", "cal_default")}'
new = 'return {k: u[k] for k in ("username", "staff_id", "display_name", "must_change", "is_admin") if k in u} | {"default_tab": u.get("default_tab") or "cal", "cal_default": u.get("cal_default", True)}'
assert old in src
src = src.replace(old, new, 1)
f.write_text(src, encoding="utf-8")
print("OK")
