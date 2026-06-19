#!/usr/bin/env python

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
import json
import os


bg_colours = {}
with open("manual/background-colours.json") as f:
	bg_colours = json.load(f)

chars = []
with open("automatic/characters.genshin-wiki.json") as f:
	chars = json.load(f)

base_uri = "https://genshin-impact.fandom.com/wiki/"

for i, char in enumerate(chars):
	lower_key = char["key"].lower()

	if os.path.exists(f"automatic/characters/{lower_key}.json"):
		continue

	sleep(20)
	print(f"Scraping {char['key']} ({i + 1}/{len(chars)})")

	options = Options()
	options.add_argument("--headless=new")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	options.binary_location = "/usr/bin/google-chrome-stable"

	driver = webdriver.Chrome(options=options)
	try:
		driver.get(base_uri + char["key"])

		# Wait for the sidebar info table element to load
		WebDriverWait(driver, 15).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "td[data-source=quality]"))
		)

		char_soup = BeautifulSoup(driver.page_source, "html.parser")

		stars = int(char_soup.css.select_one("td[data-source=quality] img")["alt"].split(" ")[0])
		release = datetime.strptime(char_soup.css.select_one("[data-source=releaseDate] div").contents[0].strip(), "%B %d, %Y")

		character = {
			"background": bg_colours.get(lower_key, "yellow" if 5 == stars else "purple"),
			"element": char_soup.find("td", attrs={"data-source": "element"}).text.strip().lower(),
			"id": i,
			"key": lower_key,
			"name": char["key"].replace("_", " "),
			"release": release.strftime("%Y-%m-%d"),
			"roles": [role_el.text.strip().lower() for role_el in char_soup.find_all(class_="cont-inline-block")],
			"stars": stars,
			"weapon": char_soup.find("td", attrs={"data-source": "weapon"}).text.strip().lower(),
		}
		json.dump(character, open(f"automatic/characters/{lower_key}.json", "w"))

	finally:
		driver.quit()


