src = open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py").read()

old_cols = """INSERT INTO account_quotes
                    (id, account_id, fm_customer_id, job_number, record_type,
                     quote_date, job_date, date_shipped, sales_person, buyer_name,
                     customer_name, project, enduser_ref, po_number, invoice_number,
                     invoice_date, billing_terms, job_status, clamps_total,
                     pipejacks_total, specialty_total, total_amount, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"""

new_cols = """INSERT INTO account_quotes
                    (id, account_id, fm_customer_id, job_number, record_type,
                     quote_date, job_date, date_shipped, sales_person, buyer_name,
                     customer_name, project, enduser_ref, po_number, invoice_number,
                     invoice_date, billing_terms, job_status,
                     billing_address, billing_city, billing_state, billing_zip,
                     clamps_total, pipejacks_total, specialty_total, total_amount, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"""

assert old_cols in src, "INSERT not found"
src = src.replace(old_cols, new_cols, 1)

# Also fix ON CONFLICT SET to include address fields
old_conflict = "job_status=EXCLUDED.job_status,\n                    billing_address=EXCLUDED.billing_address"
if old_conflict not in src:
    old_conf2 = "job_status=EXCLUDED.job_status,\n                    clamps_total=EXCLUDED.clamps_total"
    new_conf2 = "job_status=EXCLUDED.job_status,\n                    billing_address=EXCLUDED.billing_address, billing_city=EXCLUDED.billing_city,\n                    billing_state=EXCLUDED.billing_state, billing_zip=EXCLUDED.billing_zip,\n                    clamps_total=EXCLUDED.clamps_total"
    assert old_conf2 in src, "conflict clause not found"
    src = src.replace(old_conf2, new_conf2, 1)
    print("Fixed conflict clause")

import ast
ast.parse(src)
open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py", "w").write(src)
print("Saved OK")
import re
m = re.search(r"INSERT INTO account_quotes.*?ON CONFLICT", src, re.S)
ps = src[m.start():m.end()].count("%s")
print(f"%s count: {ps}")
