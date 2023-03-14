#!/usr/bin/env python

from datetime import datetime
import json
import os

json_data = {
    "version": int(datetime.today().strftime("%y%m%d"))
}

out_file = "output/data.json"

try:
    # Try to backup the previous version
    f = open(out_file)
    old_json_ver = json.load(f)["version"]
    f.close()
    os.rename(out_file, f"output/data.v{old_json_ver}.json")
except Exception:
    pass
finally:
    # Write current version
    f = open(out_file, "w")
    f.write(json.dumps(json_data))
    f.close()
