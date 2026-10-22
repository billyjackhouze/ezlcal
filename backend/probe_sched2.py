import urllib.request, json, base64, ssl, os, urllib.parse
from dotenv import load_dotenv; from pathlib import Path
load_dotenv(Path(r'C:\apps\ezlcal\backend\.env'))
host='https://fms26.alamark.com'; db='ez-line'
b64=base64.b64encode(f"{os.environ['FM_USER']}:{os.environ['FM_PASSWORD']}".encode()).decode()
ctx=ssl.create_default_context()
req=urllib.request.Request(f'{host}/fmi/data/v1/databases/{db}/sessions',method='POST',data=b'{}',headers={'Authorization':f'Basic {b64}','Content-Type':'application/json'})
token=json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())['response']['token']
url=f'{host}/fmi/data/v1/databases/{db}/layouts/SCHEDULE/records?_limit=1'
req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}'})
data=json.loads(urllib.request.urlopen(req,timeout=20,context=ctx).read())
fd=data['response']['data'][0]['fieldData']
for k in sorted(fd.keys()): print(f'  {repr(k)}: {repr(str(fd[k])[:50])}')
