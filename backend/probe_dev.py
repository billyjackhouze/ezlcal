import urllib.request, json, base64, ssl, urllib.parse, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
host = os.environ["FM_HOST"]
db = os.environ["FM_DB"]
user = os.environ["FM_USER"]
pw = os.environ["FM_PASSWORD"]
ctx = ssl.create_default_context()
b64 = base64.b64encode(f"{user}:{pw}".encode()).decode()
req = urllib.request.Request(
    f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions",
    method="POST", data=b"{}",
    headers={"Authorization": f"Basic {b64}", "Content-Type": "application/json"}
)
token = json.loads(urllib.request.urlopen(req, timeout=15, context=ctx).read())["response"]["token"]
print(f"Logged in to {db}")
for layout in ["API_CRM_Accounts", "API_BUYER", "API_CRM_BuyerAccount", "CRM_AccountOffice"]:
    url = f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/layouts/{urllib.parse.quote(layout)}/records?_limit=1"
    req2 = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = json.loads(urllib.request.urlopen(req2, timeout=15, context=ctx).read())
        ct = resp["response"]["dataInfo"]["foundCount"]
        print(f"  {layout}: OK ({ct} records)")
    except Exception as e:
        print(f"  {layout}: FAILED - {e}")
urllib.request.urlopen(urllib.request.Request(
    f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/sessions/{token}",
    method="DELETE", headers={"Authorization": f"Bearer {token}"}
), timeout=10, context=ctx)
