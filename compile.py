#!/usr/bin/env python

from datetime import datetime
from utils import list_flatten, list_uniques, get_character_id
import glob
import json
import os
import pandas as pd


json_data = {
	"version": int(datetime.today().strftime("%y%m%d")),
	"characters": {},
}

# Load characters list from JSON
with open("automatic/characters.genshin-wiki.json") as f:
	chars = json.load(f)
	# json_data["characters"] = dict((get_character_id(c["key"], "anemo"), c) for c in chars)
	characters = dict((c["key"].lower(), c) for c in chars)

	index = 0
	for character_id, character in characters.items():
		with open(f"automatic/characters/{character_id.lower()}.json") as f:
			characterData = json.load(f)

			if character_id == "traveler":
				for element in ["anemo", "geo", "electro", "dendro", "hydro", "pyro"]:
					json_data["characters"][f"traveler_{element}"] = {
						**character,
						**characterData,
						"id": index,
						"element": element,
					}
					index += 1
			else:
				json_data["characters"][character_id] = {
					**character,
					**characterData,
					"id": index,
				}
				index += 1


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


# def parse_presets():
# 	df_presets = pd.read_json("automatic/presets.gottsmillk.json")

# 	for character_id in list_uniques(list_flatten([df_presets[col].unique() for col in df_presets])):
# 		is_known_char = character_id in json_data["characters"] and "id" in json_data["characters"][character_id]
# 		numeric_id = json_data["characters"][character_id]["id"] if is_known_char else None
# 		df_presets.replace({character_id: numeric_id}, inplace=True)

# 	df_presets.dropna(inplace=True)
# 	return df_presets.astype(int).values.tolist()

# Presets are currently disabled
# json_data["presets"] = parse_presets()
json_data["presets"] = []

with open("manual/reactions.json") as f:
	json_data["reactions"] = json.load(f)

with open("manual/spritesheets.json") as f:
	json_data["spritesheets"] = json.load(f)

with open("manual/assets.json") as f:
	json_data["assets"] = json.load(f)

# with open("manual/renames.json") as f:
# 	renames = json.load(f)

# 	for character_id in json_data["characters"]:
# 		name = json_data["characters"][character_id]["name"]

# 		if name in renames:
# 			json_data["characters"][character_id]["name"] = renames[name]

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
