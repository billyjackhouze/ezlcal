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
# Try Customer_Order_blank layout - get one record and show all fields
url = f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/layouts/Customer_Order_blank/records?_limit=1"
req2 = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
try:
    resp = json.loads(urllib.request.urlopen(req2, timeout=30, context=ctx).read())
    fd = resp["response"]["data"][0]["fieldData"]
    addr_fields = {k: v for k, v in fd.items() if any(x in k.lower() for x in ["addr", "city", "state", "zip", "street", "ship", "mail"])}
    print("Address-related fields on Customer_Order_blank:")
    for k, v in sorted(addr_fields.items()):
        print(f"  {k!r}: {repr(str(v)[:60])}")
except Exception as e:
    print(f"FAILED: {e}")
