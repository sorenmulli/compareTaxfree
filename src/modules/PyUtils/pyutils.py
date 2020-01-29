
def floatify_dk_num(number_as_string: str):
	return float((number_as_string.replace(".", "")).replace(",", "."))
	
def alphabetize(composite_str: str):
	return ''.join(filter(str.isalnum, composite_str))