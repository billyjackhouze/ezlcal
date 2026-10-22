src = open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py").read()

# Find and fix the INSERT statement - count columns and match placeholders
# The INSERT should have exactly these columns:
# id, account_id, fm_customer_id, job_number, record_type,
# quote_date, job_date, date_shipped, sales_person, buyer_name,
# customer_name, project, enduser_ref, po_number, invoice_number,
# invoice_date, billing_terms, job_status, billing_address, billing_city,
# billing_state, billing_zip, clamps_total, pipejacks_total, specialty_total,
# total_amount, updated_at(=now())
# That is 26 %s + now()

import re

# Fix VALUES line - replace any existing VALUES (%s...) with correct count
old = re.search(r'VALUES \((%s,?)+,?now\(\)\)', src)
if old:
    print(f"Found: {old.group()[:80]}")
    correct = "VALUES (" + ",".join(["%s"]*26) + ",now())"
    src = src[:old.start()] + correct + src[old.end():]
    print(f"Fixed to: {correct[:80]}")

import ast
try:
    ast.parse(src)
    open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py", "w").write(src)
    print("Saved OK")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
