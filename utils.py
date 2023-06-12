def string_to_snake(s):
	return s.lower().replace(" ", "_")


def list_flatten(lst):
	return [item for sublist in lst for item in sublist]


def list_uniques(lst):
	return list(dict.fromkeys(lst))


def get_character_id(name):
	try:
		# Known aliases
		return {
			"Ayaka": "kamisato_ayaka",
			"Ayato": "kamisato_ayato",
			"Baizhuer": "baizhu",
			"Childe": "tartaglia",
			"Heizou": "shikanoin_heizou",
			"Itto": "arataki_itto",
			"Kazuha": "kaedehara_kazuha",
			"Kokomi": "sangonomiya_kokomi",
			"Raiden": "raiden_shogun",
			"Sara": "kujou_sara",
			"Shinobu": "kuki_shinobu",
			"Yae": "yae_miko",
			"Yan Fei": "yanfei",
		}[name]
	except KeyError:
		snake = string_to_snake(name)

		# Be aware of this when importing this function anywhere new
		if name.startswith("Traveler"):
			if "(" in name: # Genshin.gg format
				return snake.replace("(", "").replace(")", "")
			else: # Gottsmillk's scrapers' format
				return "traveler_" + snake[8:]

		return snake
