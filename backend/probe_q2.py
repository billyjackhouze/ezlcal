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
for layout in ['QUOTE HEADER Blank','Quotes','Quotes by Customer Detail']:
    try:
        url=f'{host}/fmi/data/v1/databases/{db}/layouts/{urllib.parse.quote(layout)}/records?_limit=1'
        import urllib.parse
        req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}'})
        data=json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())
        if data.get('response',{}).get('data'):
            print(f'\n{layout}: {list(data["response"]["data"][0]["fieldData"].keys())}')
        else:
            print(f'\n{layout}: no data')
    except Exception as e:
        print(f'\n{layout}: ERROR {e}')
urllib.request.urlopen(urllib.request.Request(f'{host}/fmi/data/v1/databases/{db}/sessions/{token}',method='DELETE',headers={'Authorization':f'Bearer {token}'}),timeout=10,context=ctx)
