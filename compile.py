#!/usr/bin/env python

from datetime import datetime
import glob
import json
import os
import warnings


def to_snake(s):
	return s.lower().replace(" ", "_")


json_data = {
	"version": int(datetime.today().strftime("%y%m%d")),
	"characters": {},
}

# Load characters' data from JSON
with open("automatic/characters.genshindev-api.json") as f:
	chars = json.load(f)
	characters_data = dict((to_snake(c["name"]), c) for c in chars)

	with open("manual/release-dates.json") as f:
		release_dates = json.load(f)

		for character_id in release_dates:
			subs_character_id = "traveler" if character_id.startswith("traveler") else character_id

			if (subs_character_id not in characters_data):
				warnings.warn(f"Data for character ID {subs_character_id} is missing")

				json_data["characters"][character_id] = {
					"release": release_dates[character_id]
				}

				continue

			json_data["characters"][character_id] = characters_data[subs_character_id]
			json_data["characters"][character_id]["release"] = release_dates[character_id]


def extract_tierlist(path):
	f = open(path)
	json_data = json.load(f)
	f.close()
	return json_data


JSONs = glob.glob("./automatic/tierlist*.json")
tier_lists = [extract_tierlist(JSON) for JSON in JSONs]

for character_id, score in tier_lists[0].items():
	json_data["characters"][character_id]["score"] = score

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
