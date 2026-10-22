import urllib.request, json, base64, ssl, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r'C:\apps\ezlcal\backend\.env'))
host='https://fms26.alamark.com'; db='ez-line'
user=os.environ['FM_USER']; pw=os.environ['FM_PASSWORD']
ctx=ssl.create_default_context()
b64=base64.b64encode(f'{user}:{pw}'.encode()).decode()
req=urllib.request.Request(f'{host}/fmi/data/v1/databases/{db}/sessions',method='POST',data=b'{}',headers={'Authorization':f'Basic {b64}','Content-Type':'application/json'})
token=json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())['response']['token']
url=f'{host}/fmi/data/v1/databases/{db}/layouts/API_Quote_Header/records?_limit=2'
req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}'})
data=json.loads(urllib.request.urlopen(req,timeout=30,context=ctx).read())
if data.get('response',{}).get('data'):
    print('Fields:',list(data['response']['data'][0]['fieldData'].keys()))
    for r in data['response']['data']: print(json.dumps(r['fieldData'],default=str))
urllib.request.urlopen(urllib.request.Request(f'{host}/fmi/data/v1/databases/{db}/sessions/{token}',method='DELETE',headers={'Authorization':f'Bearer {token}'}),timeout=10,context=ctx)
