import re
content = open('app/fmsync.py', encoding='utf-8').read()
# fix any f-string that got split: f"\n== becomes f"==
content = re.sub(r'print\(f"\\n', 'print(f"', content)
# also fix any literal newline inside an f-string on a print line
content = re.sub(r'print\(f"\n', 'print(f"', content)
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
