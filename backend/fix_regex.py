import re
content = open('app/fmsync.py', encoding='utf-8').read()
content = content.replace(
    r'out={TYPE_CODES.get(t.strip().lower(),"") for t in re.split(r"[',
    'out={TYPE_CODES.get(t.strip().lower(),"") for t in re.split(r"[\\r\\n]+'
)
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
