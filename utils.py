def string_to_snake(s):
	return s.lower().replace(" ", "_")


def list_flatten(lst):
	return [item for sublist in lst for item in sublist]


def list_uniques(lst):
	return list(dict.fromkeys(lst))
