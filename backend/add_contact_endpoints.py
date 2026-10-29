from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")
if "/contacts/{contact_id}/quotes" in src:
    print("Already exists")
else:
    marker = "# ---------- global quotes and jobs ----------"
    ep = """
@app.get("/api/contacts/{contact_id}/quotes")
def get_contact_quotes(contact_id: str, u: dict = Depends(current_user)):
    with pool.connection() as c:
        nm = c.execute("SELECT name FROM contacts WHERE id=%s", (contact_id,)).fetchone()
        if not nm: raise HTTPException(404, "Not found")
        rows = c.execute(
            "SELECT job_number,quote_date,job_date,sales_person,buyer_name,customer_name,"
            "project,total_amount,record_type,fm_customer_id FROM account_quotes "
            "WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type='quote' "
            "ORDER BY coalesce(quote_date,job_date) DESC NULLS LAST LIMIT 200",
            (nm["name"],)).fetchall()
        totals = c.execute(
            "SELECT extract(year from coalesce(quote_date,job_date))::int AS yr,"
            "sum(total_amount) AS total FROM account_quotes "
            "WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type='quote' "
            "AND coalesce(quote_date,job_date) IS NOT NULL GROUP BY yr ORDER BY yr DESC LIMIT 4",
            (nm["name"],)).fetchall()
    return {"rows":[dict(r) for r in rows],
            "totals":{str(int(t["yr"])):float(t["total"] or 0) for t in totals if t["yr"]}}

@app.get("/api/contacts/{contact_id}/jobs")
def get_contact_jobs(contact_id: str, u: dict = Depends(current_user)):
    with pool.connection() as c:
        nm = c.execute("SELECT name FROM contacts WHERE id=%s", (contact_id,)).fetchone()
        if not nm: raise HTTPException(404, "Not found")
        rows = c.execute(
            "SELECT job_number,quote_date,job_date,sales_person,buyer_name,customer_name,"
            "project,total_amount,record_type,fm_customer_id FROM account_quotes "
            "WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type='job' "
            "ORDER BY coalesce(job_date,quote_date) DESC NULLS LAST LIMIT 200",
            (nm["name"],)).fetchall()
        totals = c.execute(
            "SELECT extract(year from coalesce(job_date,quote_date))::int AS yr,"
            "sum(total_amount) AS total FROM account_quotes "
            "WHERE upper(trim(buyer_name))=upper(trim(%s)) AND record_type='job' "
            "AND coalesce(job_date,quote_date) IS NOT NULL GROUP BY yr ORDER BY yr DESC LIMIT 4",
            (nm["name"],)).fetchall()
    return {"rows":[dict(r) for r in rows],
            "totals":{str(int(t["yr"])):float(t["total"] or 0) for t in totals if t["yr"]}}

"""
    assert marker in src
    src = src.replace(marker, ep + marker, 1)
    f.write_text(src, encoding="utf-8")
    print("OK: endpoints added")
