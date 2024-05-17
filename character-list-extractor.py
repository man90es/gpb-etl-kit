#!env python

from dotenv import dotenv_values
from utils import get_character_id
import json
import requests


bg_colours = {}
with open("manual/background-colours.json") as f:
	bg_colours = json.load(f)


def extract_character(json_data, i):
	element = json_data["vision"].lower()
	char_id = get_character_id(json_data["name"], element)
	bg = bg_colours.get(char_id, "yellow" if 5 == json_data["rarity"] else "purple")

	return {
		"background": bg,
		"element": element,
		"id": i,
		"name": json_data["name"],
		"release": json_data["release"],
		"stars": json_data["rarity"],
		"weapon": json_data["weapon"].lower(),
	}


uri = dotenv_values(".env")["GENSHINDEV_API_URI"] + "/characters/all"
res = requests.get(uri).json()

characters = [extract_character(JSON, i) for i, JSON in enumerate(res)]

json.dump(characters, open("automatic/characters.genshindev-api.json", "w"))
