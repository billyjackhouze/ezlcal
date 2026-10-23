from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")
endpoint = """
@app.put("/api/staff/{staff_id}/color")
def set_staff_color(staff_id: str, body: dict, u: dict = Depends(current_user)):
    if not u.get("is_admin"):
        raise HTTPException(403, "Admin only")
    color = (body.get("color") or "").strip()[:20]
    with pool.connection() as c:
        c.execute("ALTER TABLE staff ADD COLUMN IF NOT EXISTS cal_color TEXT")
        n = c.execute("UPDATE staff SET cal_color=%s WHERE id=%s", (color or None, staff_id)).rowcount
    if not n:
        raise HTTPException(404, "Staff not found")
    return {"ok": True}

"""
marker = "\n# ---------- global quotes and jobs ----------"
if "/api/staff/" not in src and marker in src:
    src = src.replace(marker, endpoint + marker, 1)
    f.write_text(src, encoding="utf-8")
    print("OK: endpoint added")
elif "/api/staff/" in src:
    print("Already exists")
else:
    print("MISS:", marker[:40])
