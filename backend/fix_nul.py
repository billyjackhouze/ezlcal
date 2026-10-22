import re
content = open('app/fmsync.py', encoding='utf-8').read()
content = re.sub(r'def s\(v\):\n    return "" if v is None else str\(v\)\.strip\(\)', 'def s(v):\n    return "" if v is None else str(v).strip().replace(chr(0), "")', content)
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
