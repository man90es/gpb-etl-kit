#!env python

from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import json
import os
import requests


bg_colours = {}
with open("manual/background-colours.json") as f:
	bg_colours = json.load(f)

char_keys = []
with open("automatic/characters.genshin-wiki.json") as f:
	char_keys = json.load(f)

base_uri = "https://genshin-impact.fandom.com/wiki/"

for i, char_key in enumerate(char_keys):
	lower_key = char_key.lower()

	if os.path.exists(f"automatic/characters/{lower_key}.json"):
		continue

	sleep(5)
	print(f"Scraping {char_key} ({i + 1}/{len(char_keys)})")
	page = requests.get(base_uri + char_key)
	char_soup = BeautifulSoup(page.content, "html.parser")

	stars = int(char_soup.css.select_one("td[data-source=quality] img")["alt"].split(" ")[0])
	release = datetime.strptime(char_soup.css.select_one("[data-source=releaseDate] div").contents[0].strip(), "%B %d, %Y")

	character = {
		"background": bg_colours.get(lower_key, "yellow" if 5 == stars else "purple"),
		"element": char_soup.find("td", attrs={"data-source": "element"}).text.strip().lower(),
		"id": i,
		"key": lower_key,
		"name": char_key.replace("_", " "),
		"release": release.strftime("%Y-%m-%d"),
		"roles": [role_el.text.strip().lower() for role_el in char_soup.find_all(class_="cont-inline-block")],
		"stars": stars,
		"weapon": char_soup.find("td", attrs={"data-source": "weapon"}).text.strip().lower(),
	}
	json.dump(character, open(f"automatic/characters/{lower_key}.json", "w"))
