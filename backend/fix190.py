content = open('app/fmsync.py', encoding='utf-8').read()
content = content.replace('print(f"\n== {LAYOUTS[kind]} ({kind})")', 'print(f"== {LAYOUTS[kind]} ({kind})")')
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
