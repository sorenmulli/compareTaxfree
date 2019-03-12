import requests 
import json

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


scrape_url = "https://www.pricerunner.dk/public/v1/cl/1424/dk/desktop?page={}&attr_56525176=58381604&retailer=63022&urlName=%C3%98l%20og%20spiritus&sort=1"

all_products = list()
	
for i in range(1, 10000):
	r = requests.get(scrape_url.format(i)).json()
	
	prods = r["viewData"]["category"]["products"]
	if prods is None:
		break
	clean_prods = list()
	
	for prod in prods:
		clean_prod = {}
		
		clean_prod["name"] = prod["name"]
		clean_prod["price"] = prod["localMinPrice"]["value"]
		
#			try:
#				clean_prod["shipping"] = prod["shippingCost"]["amount"]	
#			except TypeError:
#				clean_prod["shipping"] = None	
					
		clean_prods.append(clean_prod)
	all_products += clean_prods
		
	print(len(all_products))
with open("pricerunner_prices.json", 'w+') as outfile:
	json.dump(all_products, outfile)