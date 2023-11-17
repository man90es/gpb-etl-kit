#!/usr/bin/env python

from datetime import datetime
from utils import list_flatten, list_uniques, get_character_id
import glob
import json
import os
import pandas as pd
import warnings


json_data = {
	"version": int(datetime.today().strftime("%y%m%d")),
	"characters": {},
}

# Load characters' data from JSON
with open("automatic/characters.genshindev-api.json") as f:
	chars = json.load(f)
	characters_data = dict((get_character_id(c["name"], c["element"]), c) for c in chars)

	with open("manual/roles.json") as f:
		roles = json.load(f)

		for character_id in characters_data:
			json_data["characters"][character_id] = characters_data[character_id]

			if (character_id in roles):
				json_data["characters"][character_id]["roles"] = roles[character_id]
			else:
				warnings.warn(f"Roles data for character ID {character_id} is missing")


def extract_tierlist(path):
	f = open(path)
	json_data = json.load(f)
	f.close()
	return json_data


JSONs = glob.glob("./automatic/tierlist*.json")
tier_lists = [extract_tierlist(JSON) for JSON in JSONs]

for character_id, character in json_data["characters"].items():
	default_score = [7.5 if 5 == character["stars"] else 5] * 7
	# TODO: Merge scores from multiple tier lists
	score = tier_lists[0].get(character_id, default_score)
	json_data["characters"][character_id]["score"] = score


def parse_presets():
	df_presets = pd.read_json("automatic/presets.gottsmillk.json")

	for character_id in list_uniques(list_flatten([df_presets[col].unique() for col in df_presets])):
		is_known_char = character_id in json_data["characters"] and "id" in json_data["characters"][character_id]
		numeric_id = json_data["characters"][character_id]["id"] if is_known_char else None
		df_presets.replace({character_id: numeric_id}, inplace=True)

	df_presets.dropna(inplace=True)
	return df_presets.astype(int).values.tolist()


json_data["presets"] = parse_presets()

with open("manual/reactions.json") as f:
	json_data["reactions"] = json.load(f)

with open("manual/spritesheets.json") as f:
	json_data["spritesheets"] = json.load(f)

with open("manual/renames.json") as f:
	renames = json.load(f)

	for character_id in json_data["characters"]:
		name = json_data["characters"][character_id]["name"]

		if name in renames:
			json_data["characters"][character_id]["name"] = renames[name]

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
	f.write(json.dumps(json_data, separators=(",", ":")))
	f.close()
