#!env python

import glob
import json
import numpy as np
import os
import pandas as pd


def to_snake(s):
	return s.lower().replace(" ", "_")


def get_character_id(name):
	try:
		return {
			"Ayaka": "kamisato_ayaka",
			"Ayato": "kamisato_ayato",
			"Baizhuer": "baizhu",
			"Heizou": "shikanoin_heizou",
			"Itto": "arataki_itto",
			"Kazuha": "kaedehara_kazuha",
			"Kokomi": "sangonomiya_kokomi",
			"Raiden": "raiden_shogun",
			"Sara": "kujou_sara",
			"Shinobu": "kuki_shinobu",
			"Yae": "yae_miko",
		}[name]
	except KeyError:
		if name.startswith("Traveler"):
			return "traveler_" + to_snake(name[8:])

		return to_snake(name).replace("(", "").replace(")", "")


def flatten(lst):
	return [item for sublist in lst for item in sublist]


def list_uniques(lst):
	return list(dict.fromkeys(lst))


# Execute Gottsmillk's scraping scripts
os.chdir("./submodules/genshin-spiral-abyss-teams-compilation")

scripts = [
	{
		"name": "gcim",
		"path": "genshin_teams_aggregation_from_gcsim.py",
	},
	{
		"name": "Spiral Stats",
		"path": "genshin_teams_aggregation_from_spiral_stats.py",
	},
	{
		"name": "AkashaData",
		"path": "genshin_teams_aggregation_from_akashadata.py",
	},
	{
		"name": "Mihoyo",
		"path": "genshin_teams_aggregation_from_mihoyo.py",
	},
]

for script in scripts:
	try:
		exec(open(script['path']).read())
	except Exception:
		print(f"Failed fetching team presets from {script['name']}")

os.chdir("../..")

# Read CSV data
scraped_teams_files = glob.glob("./submodules/genshin-spiral-abyss-teams-compilation/inputs/*.csv")
named_teams_files = glob.glob("./submodules/genshin-spiral-abyss-teams-compilation/genshinTeamsNamed*.csv")
df_scraped = pd.concat((pd.read_csv(f, names=range(4)) for f in scraped_teams_files), ignore_index=True)
df_named = pd.concat((pd.read_csv(f, usecols=range(4), names=range(5)) for f in named_teams_files), ignore_index=True)
df = pd.concat((df_scraped, df_named), ignore_index=True)

# Drop Traveller with no specified element
df.replace("Traveler", None, inplace=True)

# Remove parties with missing members and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Sort teams
data = df.to_numpy()
sorted_np = np.sort(data)
df = pd.DataFrame(sorted_np, columns=range(4)).astype("string")

# Remove parties with missing members and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

for name in list_uniques(flatten([df[col].unique() for col in df])):
	character_id = get_character_id(name)
	df.replace({name: character_id}, inplace=True)

# Write to file
json.dump(df.values.tolist(), open("automatic/presets.gottsmillk.json", "w"), sort_keys=True)
