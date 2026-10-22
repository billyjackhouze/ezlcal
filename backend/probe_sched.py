import urllib.request, json, base64, ssl, os, urllib.parse
from dotenv import load_dotenv; from pathlib import Path
load_dotenv(Path(r'C:\apps\ezlcal\backend\.env'))
host='https://fms26.alamark.com'; db='ez-line'
b64=base64.b64encode(f"{os.environ['FM_USER']}:{os.environ['FM_PASSWORD']}".encode()).decode()
ctx=ssl.create_default_context()
req=urllib.request.Request(f'{host}/fmi/data/v1/databases/{db}/sessions',method='POST',data=b'{}',headers={'Authorization':f'Basic {b64}','Content-Type':'application/json'})
token=json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())['response']['token']
for layout in ['SCHEDULE','Customer_Order_Totals','Customer_Order_List']:
    try:
        url=f'{host}/fmi/data/v1/databases/{db}/layouts/{urllib.parse.quote(layout)}/records?_limit=1'
        req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}'})
        data=json.loads(urllib.request.urlopen(req,timeout=20,context=ctx).read())
        if data.get('response',{}).get('data'):
            fd=data['response']['data'][0]['fieldData']
            print(f'\n{layout} ({len(fd)} fields): {sorted(fd.keys())[:15]}')
            print('Sample:', {k:v for k,v in list(fd.items())[:6]})
        else:
            print(f'\n{layout}: no records')
    except Exception as e: print(f'\n{layout}: {type(e).__name__}: {str(e)[:80]}')
