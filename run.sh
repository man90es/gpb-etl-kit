#!/bin/sh

git submodule foreach 'git pull'

env python ./genshin-gg-tierlist-scraper.py
env python ./character-list-extractor.py
env python ./teams-scraper.py
env python ./compile.py

echo 'data.json generated'
