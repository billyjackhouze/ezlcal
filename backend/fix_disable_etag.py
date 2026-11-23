from pathlib import Path
f = Path(r"C:\Apps\ezlcal\backend\app\main.py")
src = f.read_text(encoding="utf-8")

# Comment out the 304 return so every request gets fresh data
old = '        if if_none_match == etag:\n            return Response(status_code=304, headers={"ETag": etag})'
new = '        # if if_none_match == etag:\n        #     return Response(status_code=304, headers={"ETag": etag})'
if old in src:
    src = src.replace(old, new, 1)
    print("OK: ETag cache disabled")
else:
    print("MISS")

f.write_text(src, encoding="utf-8")
print("Done")
