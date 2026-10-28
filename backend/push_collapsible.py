# Download the updated index.html from sandbox and deploy it
import urllib.request, shutil
from pathlib import Path

url = "https://raw.githubusercontent.com/billyjackhouze/ezlcal/88337bd/web/index.html"
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        content = r.read().decode("utf-8")
    if "toggleBox" not in content:
        print("ERROR: toggleBox not in downloaded file - wrong commit")
    else:
        utf8nobom = "utf-8-sig"
        for p in [r"C:\Apps\ezlcal\backend\dist\index.html", r"C:\Apps\ezlcal\web\index.html"]:
            Path(p).write_text(content, encoding="utf-8")
        print(f"OK: deployed {len(content)} chars, collapsible={content.count('collapsible')}")
except Exception as e:
    print(f"Download failed: {e}")
    print("Try manual copy instead")
