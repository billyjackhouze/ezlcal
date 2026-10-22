import re

src = open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py").read()

# 1. Add billing address columns to account_quotes table
old_schema = '"    invoice_date    DATE,\n"'
new_schema = '"    invoice_date    DATE,\n"' + \
    '"    billing_address TEXT,\n"' + \
    '"    billing_city    TEXT,\n"' + \
    '"    billing_state   TEXT,\n"' + \
    '"    billing_zip     TEXT,\n"'
src = src.replace(old_schema, new_schema, 1)

# 2. Add ALTER TABLE for new columns
old_alter = '("invoice_number", "TEXT"), ("invoice_date", "DATE"),'
new_alter = '("invoice_number", "TEXT"), ("invoice_date", "DATE"), ("billing_address", "TEXT"), ("billing_city", "TEXT"), ("billing_state", "TEXT"), ("billing_zip", "TEXT"),'
src = src.replace(old_alter, new_alter, 1)

# 3. Add address fields to upsert_rows tuple
old_row = 's(r.get("JOB_Status")),\n            num(r.get("CLAMPS'
new_row = 's(r.get("JOB_Status")),\n            s(r.get("schedule.QUOTE_HEADER|quote_header_ID.primary::Billing Address")),\n            s(r.get("schedule.QUOTE_HEADER|quote_header_ID.primary::Billing City")),\n            s(r.get("schedule.QUOTE_HEADER|quote_header_ID.primary::Billing State")),\n            s(r.get("schedule.QUOTE_HEADER|quote_header_ID.primary::Billing Zip")),\n            num(r.get("CLAMPS'
src = src.replace(old_row, new_row, 1)

# 4. Add columns to INSERT
old_insert = '"     quote_date, job_date, date_shipped, sales_person, buyer_name,"\n            " customer_name, project, enduser_ref, po_number, invoice_number,"\n            " invoice_date, billing_terms, job_status, clamps_total,"'
new_insert = '"     quote_date, job_date, date_shipped, sales_person, buyer_name,"\n            " customer_name, project, enduser_ref, po_number, invoice_number,"\n            " invoice_date, billing_terms, job_status, billing_address, billing_city,"\n            " billing_state, billing_zip, clamps_total,"'
src = src.replace(old_insert, new_insert, 1)

# 5. Fix VALUES placeholders - count current %s and add 4 more
# Find the VALUES line and add 4 more %s
old_vals = '            " LIMIT 5000"\n        ).fetchall()'
# Just find INSERT VALUES line
lines = src.split("\n")
for i, line in enumerate(lines):
    if "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())" in line:
        lines[i] = line.replace(
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())",
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        )
        break
src = "\n".join(lines)

# 6. Add to ON CONFLICT UPDATE
old_conflict = "job_status=EXCLUDED.job_status,\n                    clamps_total"
new_conflict = "job_status=EXCLUDED.job_status,\n                    billing_address=EXCLUDED.billing_address, billing_city=EXCLUDED.billing_city,\n                    billing_state=EXCLUDED.billing_state, billing_zip=EXCLUDED.billing_zip,\n                    clamps_total"
src = src.replace(old_conflict, new_conflict, 1)

open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py", "w").write(src)
print("patch applied")

# verify
import ast
try:
    ast.parse(src)
    print("syntax OK")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
