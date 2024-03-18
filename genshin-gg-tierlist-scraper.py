#!env python

from bs4 import BeautifulSoup
from utils import get_character_id
import json
import requests


def parse_constellation(str):
	return int(str[-1]) if str[-1].isdigit() else 0


c_limits = {}
with open("manual/constellation-limits.json") as f:
	c_limits = json.load(f)

uri = "https://genshin.gg/tier-list/"
page = requests.get(uri)

soup = BeautifulSoup(page.content, "html.parser")
tier_elements = soup.find_all("div", class_="dropzone-row")

chars = {}

for i, tier_element in enumerate(tier_elements):
	internal_tier_element = tier_element.find(class_="dropzone-characters")

	max_rating = (len(tier_elements) - i) * 10 / len(tier_elements)
	min_rating = (max_rating - 10 / len(tier_elements))

	for char_el in internal_tier_element.find_all(class_="tierlist-icon-wrapper"):
		c = parse_constellation(char_el.find(class_="tierlist-constellation").text)
		char_id = get_character_id(char_el.find(class_="tierlist-icon")["alt"])
		c_limit = c_limits.get(char_id, 7)
		chars[char_id] = [min_rating if j < c else max_rating for j in range(c_limit)]


json.dump(chars, open("automatic/tierlist.genshin-gg.json", "w"))
