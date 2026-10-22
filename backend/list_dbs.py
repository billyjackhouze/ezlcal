import urllib.request, json, base64, ssl
host = "https://fms26.alamark.com"
user = "WebApp"
pw = "EZLineCRMApp26!"
ctx = ssl.create_default_context()
b64 = base64.b64encode((user+":"+pw).encode()).decode()
req = urllib.request.Request(host+"/fmi/data/v1/databases",headers={"Authorization":"Basic "+b64})
try:
    resp = json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read())
    for db in resp["response"]["databases"]:
        print(db["name"])
except Exception as e:
    print("FAILED: "+str(e))
