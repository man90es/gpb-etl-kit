#!/usr/bin/env python

from datetime import datetime
import json
import os


def to_snake(s):
	return s.lower().replace(" ", "_")


json_data = {
	"version": int(datetime.today().strftime("%y%m%d"))
}

# Load characters' data from JSON
with open("automatic/characters.genshindev-api.json") as f:
	chars = json.load(f)
	json_data["characters"] = dict((to_snake(c["name"]), c) for c in chars)

out_file = "output/data.json"

# Try to backup the previous version and write a new version
try:
	with open(out_file) as f:
		old_ver = json.load(f)["version"]

	os.rename(out_file, f"output/data.v{old_ver}.json")
except Exception:
	pass
finally:
	f = open(out_file, "w")
	f.write(json.dumps(json_data))
	f.close()
