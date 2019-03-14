import json

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

with open("raw_bordershop_prices.json", 'r') as infile:
	data = json.load(infile)


