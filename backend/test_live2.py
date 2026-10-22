import urllib.request, json, base64, ssl, urllib.parse
host = "https://fms26.alamark.com"
user = "WebApp"
pw = "EZLineCRMApp26!"
db = "EZLine_CRM_Live"
ctx = ssl.create_default_context()
b64 = base64.b64encode((user+":"+pw).encode()).decode()
url = host+"/fmi/data/v1/databases/"+urllib.parse.quote(db)+"/sessions"
print("URL:", url)
req = urllib.request.Request(url,method="POST",data=b"{}",headers={"Authorization":"Basic "+b64,"Content-Type":"application/json"})
try:
    resp = json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())
    token = resp["response"]["token"]
    print("SUCCESS: "+token[:20])
    urllib.request.urlopen(urllib.request.Request(host+"/fmi/data/v1/databases/"+urllib.parse.quote(db)+"/sessions/"+token,method="DELETE",headers={"Authorization":"Bearer "+token}),timeout=10,context=ctx)
    print("Logged out.")
except Exception as e:
    print("FAILED: "+str(e))
