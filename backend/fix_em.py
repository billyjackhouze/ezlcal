src = open('app/sync_quotes.py', encoding='utf-8').read()
src = src.replace(
    'with c.transaction():\n            c.executemany("""',
    'with c.transaction(), c.cursor() as cur:\n            cur.executemany("""'
)
src = src.replace(
    '            """, upsert_rows)\n        counts = c.execute(',
    '            """, upsert_rows)\n        counts = c.execute('
)
open('app/sync_quotes.py', 'w', encoding='utf-8').write(src)
print('fixed')
