from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

# Fix quotes_ytd to use COALESCE(quote_date, job_date)
old = "COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',aq.quote_date)=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd,"
new = "COALESCE(SUM(CASE WHEN aq.record_type='quote' AND date_part('year',COALESCE(aq.quote_date,aq.job_date))=date_part('year',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd,"

if old in src:
    src = src.replace(old, new, 1)
    print("OK: quotes_ytd uses COALESCE(quote_date, job_date)")
else:
    print("MISS")

f.write_text(src, encoding="utf-8")
print("Done")
