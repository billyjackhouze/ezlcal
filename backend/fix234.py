content = open('app/fmsync.py', encoding='utf-8').read()
content = content.replace('print(f"{mode.upper()} SYNC COMPLETE\n"+json.dumps(summary,indent=2))', 'print(f"{mode.upper()} SYNC COMPLETE"); print(json.dumps(summary,indent=2))')
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
