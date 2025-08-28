#!/bin/sh

if [[ ! -d ".venv" ]]; then
	echo 'Installing dependencies'

	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	deactivate

	echo 'Fetching submodules'
	git submodule update --init --recursive
fi

source .venv/bin/activate

echo 'Updating submodules'
git submodule sync
git submodule update --remote

echo 'Running scrapers'
env python3 ./genshin-gg-tierlist-scraper.py
env python3 ./character-list-extractor.py
# None of the extractors work anymore
# env python3 ./teams-scraper.py
env python3 ./compile.py

deactivate

echo 'data.json generated'
