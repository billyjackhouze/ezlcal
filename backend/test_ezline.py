import urllib.request, json, base64, ssl
host = "https://fms26.alamark.com"
user = "WebApp"
pw = "EZLineCRMApp26!"
db = "ez-line"
ctx = ssl.create_default_context()
b64 = base64.b64encode((user+":"+pw).encode()).decode()
import urllib.parse
req = urllib.request.Request(host+"/fmi/data/v1/databases/"+urllib.parse.quote(db)+"/sessions",method="POST",data=b"{}",headers={"Authorization":"Basic "+b64,"Content-Type":"application/json"})
try:
    resp = json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())
    print("SUCCESS:", resp["response"]["token"][:20])
except Exception as e:
    print("FAILED:", e)
