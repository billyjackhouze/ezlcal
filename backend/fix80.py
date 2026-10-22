content = open('app/fmsync.py', encoding='utf-8').read()
old = '{ts_field:f">={fm_ts(since - OVERLAP)}"],"limit":PAGE,"offset":offset})'
new = '{ts_field:f">={fm_ts(since - OVERLAP)}"}],"limit":PAGE,"offset":offset})'
open('app/fmsync.py', 'w', encoding='utf-8').write(content.replace(old, new))
print('done')
