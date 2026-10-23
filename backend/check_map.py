import urllib.request, json, ssl, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
ctx = ssl.create_default_context()
# Check map endpoint directly
req = urllib.request.Request("https://ezlcal.alamark.com/api/map",
    headers={"Cookie": ""})
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    data = json.loads(resp.read())
    print(f"Offices in /api/map: {len(data.get('offices',[]))}")
    houston = [o for o in data.get('offices',[]) if o.get('state')=='TX' and 'houston' in (o.get('city') or '').lower()]
    print(f"Houston TX offices: {len(houston)}")
    if houston: print("Sample:", houston[0])
except Exception as e:
    print(f"Error: {e}")
