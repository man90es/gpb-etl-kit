#!env python

from bs4 import BeautifulSoup
import json
import requests

uri = "https://genshin.gg/tier-list/"
page = requests.get(uri)

soup = BeautifulSoup(page.content, "html.parser")
tier_elements = soup.find_all("div", class_="dropzone-row")


def to_snake(s):
	return s.lower().replace(" ", "_")


def get_character_id(name):
	try:
		return {
			"Ayaka": "kamisato_ayaka",
			"Ayato": "kamisato_ayato",
			"Childe": "tartaglia",
			"Heizou": "shikanoin_heizou",
			"Itto": "arataki_itto",
			"Kazuha": "kaedehara_kazuha",
			"Kokomi": "sangonomiya_kokomi",
			"Raiden": "raiden_shogun",
			"Sara": "kujou_sara",
		}[name]
	except KeyError:
		return to_snake(name).replace("(", "").replace(")", "")


characters = {}

for i, tier_element in enumerate(tier_elements):
	internal_tier_element = tier_element.find(class_="dropzone-characters")

	max_rating = (len(tier_elements) - i) * 10 / len(tier_elements)
	min_rating = (max_rating - 10 / len(tier_elements))

	for character_element in internal_tier_element.find_all(class_="tierlist-icon-wrapper"):
		constellation = int(character_element.find(class_="tierlist-constellation").text[-1])
		char_id = get_character_id(character_element.find(class_="tierlist-icon")["alt"])
		characters[char_id] = [min_rating if j < constellation else max_rating for j in range(7)]


json.dump(characters, open("automatic/tierlist.genshin-gg.json", "w"))
