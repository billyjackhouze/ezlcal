import re
content = open('app/fmsync.py', encoding='utf-8').read()
content = re.sub(r'def type_codes\(v\):.*?return[^\n]+', 'def type_codes(v):\n    parts = re.split(chr(13)+chr(10)+"|"+chr(13)+"|"+chr(10), str(v) if v else "")\n    out = {TYPE_CODES.get(t.strip().lower(),"") for t in parts if t.strip()}\n    return "".join(sorted(c for c in out if c))', content, flags=re.DOTALL)
open('app/fmsync.py', 'w', encoding='utf-8').write(content)
print('done')
