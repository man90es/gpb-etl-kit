#!/usr/bin/env python

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


base_uri = "https://genshin-impact.fandom.com/wiki/"
list_uri = base_uri + "Character/List"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.binary_location = "/usr/bin/google-chrome-stable"

driver = webdriver.Chrome(options=options)
char_keys = []

try:
	driver.get(list_uri)

	# Wait for the table to load on the page
	WebDriverWait(driver, 15).until(
		EC.presence_of_element_located((By.TAG_NAME, "tbody"))
	)

	soup = BeautifulSoup(driver.page_source, "html.parser")
	table_element = soup.find("tbody")

	if not table_element:
		raise Exception("Could not find character list table on page")

	for table_line in table_element.find_all("tr"):
		td = table_line.find_all("td")
		if len(td) < 1:
			continue

		char = {}

		img = td[0].find("img")
		if img:
			src = img.get("data-src") or img.get("src")
			if src:
				if src.startswith("data:") and img.get("data-src"):
					src = img.get("data-src")
				base_src = src.split("?")[0]
				if base_src[-2:].isdigit():
					char["icon"] = base_src[:-2] + "80"
				else:
					char["icon"] = base_src

		a = td[1].find("a")
		if a:
			char["key"] = a["href"].split("/")[-1]

		char_keys.append(char)

finally:
	driver.quit()

json.dump(char_keys, open("automatic/characters.genshin-wiki.json", "w"))

