#!env python

import glob
import json


def extract_character(characterJSON, i):
	f = open(characterJSON)
	json_data = json.load(f)
	f.close()

	return {
		"element": json_data["vision"].lower(),
		"id": i,
		"name": json_data["name"],
		"stars": json_data["rarity"],
		"weapon": json_data["weapon"].lower(),
	}


JSONs = glob.glob("./submodules/genshindev-api/assets/data/characters/*/en.json")
characters = [extract_character(JSON, i) for i, JSON in enumerate(JSONs)]

json.dump(characters, open("automatic/characters.genshindev-api.json", "w"))
