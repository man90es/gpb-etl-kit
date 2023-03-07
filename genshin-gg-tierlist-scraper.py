#!env python

from bs4 import BeautifulSoup
import json
import requests

uri = "https://genshin.gg/tier-list/"
page = requests.get(uri)

soup = BeautifulSoup(page.content, "html.parser")
tier_elements = soup.find_all("div", class_="dropzone-row")

characters = {}

for i, tier_element in enumerate(tier_elements):
	internal_tier_element = tier_element.find(class_="dropzone-characters")

	max_rating = (len(tier_elements) - i) * 10 / len(tier_elements)
	min_rating = (max_rating - 10 / len(tier_elements))

	for character_element in internal_tier_element.find_all(class_="tierlist-icon-wrapper"):
		constellation = int(character_element.find(class_="tierlist-constellation").text[-1])
		name = character_element.find(class_="tierlist-icon")["alt"]
		characters[name] = [min_rating if j < constellation else max_rating for j in range(7)]


json.dump(characters, open("automatic/tierlist.genshin-gg.json", "w"))
