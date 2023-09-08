#!/bin/sh

if [[ ! -d ".venv" ]]; then
	echo 'Installing dependencies'

	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	deactivate
fi

source .venv/bin/activate

echo 'Updating submodules'
git submodule foreach 'git pull'

echo 'Running scrapers'
env python ./genshin-gg-tierlist-scraper.py
env python ./character-list-extractor.py
env python ./teams-scraper.py
env python ./compile.py

deactivate

echo 'data.json generated'
