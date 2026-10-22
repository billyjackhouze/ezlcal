import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:\Apps\ezlcal\backend\.env"))
print(repr(os.environ.get("FM_LIVE_PASSWORD")))
print(repr(os.environ.get("FM_LIVE_DB")))
print(repr(os.environ.get("FM_LIVE_HOST")))
