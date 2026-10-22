import urllib.request, json, base64, ssl, urllib.parse, os
from dotenv import load_dotenv; from pathlib import Path
load_dotenv(Path(r'C:\Apps\ezlcal\backend\.env'))
host='https://fms26.alamark.com'; db='ez-line'
b64=base64.b64encode(f"{os.environ['FM_USER']}:{os.environ['FM_PASSWORD']}".encode()).decode()
ctx=ssl.create_default_context()
req=urllib.request.Request(f'{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions',method='POST',data=b'{}',headers={'Authorization':f'Basic {b64}','Content-Type':'application/json'})
token=json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())['response']['token']
url=f'{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/layouts/API_SCHEDULE/records?_limit=1'
req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}'})
data=json.loads(urllib.request.urlopen(req,timeout=30,context=ctx).read())
if data.get('response',{}).get('data'):
    fd=data['response']['data'][0]['fieldData']
    print('Fields:')
    for k,v in sorted(fd.items()): print(f'  {k}: {repr(str(v)[:60])}')
