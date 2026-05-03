#!env python

from bs4 import BeautifulSoup
import cloudscraper
import json


base_uri = "https://genshin-impact.fandom.com/wiki/"
list_uri = base_uri + "Character/List"
scraper = cloudscraper.create_scraper()
list_page = scraper.get(list_uri)

soup = BeautifulSoup(list_page.content, "html.parser")
table_element = soup.find("tbody")
char_keys = []

if not table_element:
	print(soup.prettify())
	raise Exception("Could not find character list table on page")

for table_line in table_element.find_all("tr"):
	td = table_line.find_all("td")
	if len(td) < 1:
		continue

	char = {}

	img = td[0].find("img")
	if img:
		char["icon"] = img["data-src"].split("?")[0][0:-2] + "80"

	a = td[1].find("a")
	if a:
		char["key"] = a["href"].split("/")[-1]

	char_keys.append(char)

json.dump(char_keys, open("automatic/characters.genshin-wiki.json", "w"))
