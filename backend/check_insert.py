import re
src = open(r"C:\Apps\ezlcal\backend\app\sync_quotes.py").read()
m = re.search(r"INSERT INTO account_quotes.*?ON CONFLICT", src, re.S)
if m:
    chunk = m.group()
    cols = re.findall(r"id, account_id.*?total_amount", chunk, re.S)
    vals = re.findall(r"VALUES \(([^)]+)\)", chunk)
    print("INSERT chunk:")
    print(chunk[:1500])
    ps_count = chunk.count("%s")
    print(f"\n%s count in INSERT: {ps_count}")
