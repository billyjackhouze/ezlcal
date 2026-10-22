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
req2 = urllib.request.Request(
    f"{host}/fmi/data/v1/databases/{urllib.parse.quote(db)}/layouts",
    headers={"Authorization": f"Bearer {token}"}
)
resp = json.loads(urllib.request.urlopen(req2, timeout=15, context=ctx).read())
layouts = resp["response"]["layouts"]
print(f"Layouts visible to WebApp ({len(layouts)}):")
for l in layouts:
    print(f"  {l['name']}")
