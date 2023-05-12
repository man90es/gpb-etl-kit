#!env python

import glob
import json
import numpy as np
import os
import pandas as pd

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
	except:
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

# Write to file
json.dump(df.values.tolist(), open("automatic/presets.gottsmillk.json", "w"), sort_keys=True)
