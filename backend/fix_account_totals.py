from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

old = ('"SELECT id,name,types,parent_id,root_id,sales_ytd,sales_py,quotes_ytd,last_order,address,city,state,zip,homepage"'
       '\n            " FROM accounts ORDER BY name"')

new = ('"SELECT a.id, a.name, a.types, a.parent_id, a.root_id,"'
       '\n            " COALESCE(SUM(CASE WHEN aq.record_type=\'job\' AND date_part(\'year\',aq.job_date)=date_part(\'year\',now()) THEN aq.total_amount ELSE 0 END),0) AS sales_ytd,"'
       '\n            " COALESCE(SUM(CASE WHEN aq.record_type=\'job\' AND date_part(\'year\',aq.job_date)=date_part(\'year\',now())-1 THEN aq.total_amount ELSE 0 END),0) AS sales_py,"'
       '\n            " COALESCE(SUM(CASE WHEN aq.record_type=\'quote\' AND date_part(\'year\',aq.quote_date)=date_part(\'year\',now()) THEN aq.total_amount ELSE 0 END),0) AS quotes_ytd,"'
       '\n            " a.last_order, a.address, a.city, a.state, a.zip, a.homepage"'
       '\n            " FROM accounts a"'
       '\n            " LEFT JOIN account_quotes aq ON aq.account_id=a.id"'
       '\n            " GROUP BY a.id, a.name, a.types, a.parent_id, a.root_id, a.last_order, a.address, a.city, a.state, a.zip, a.homepage"'
       '\n            " ORDER BY a.name"')

if old in src:
    src = src.replace(old, new, 1)
    print("OK: accounts query now computes totals from account_quotes")
else:
    print("MISS")
    idx = src.find("SELECT id,name,types,parent_id,root_id")
    print(repr(src[idx:idx+150]))

f.write_text(src, encoding="utf-8")
print("Done")
