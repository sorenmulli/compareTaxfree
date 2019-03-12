import requests 
import json

scrape_url = "https://www.pricerunner.dk/public/v1/cl/1424/dk/desktop?page={}&attr_56525176=58381604&retailer=63022&urlName=%C3%98l%20og%20spiritus&sort=4"


all_products = list()

with open("pricerunner_prices.json", 'w') as outfile:
	
	for i in range(1, 10000):
		r = requests.get(scrape_url.format(i)).json()
		
		prods = r["viewData"]["category"]["products"]
		if prods is None:
			break
		else:
			all_products += prods
	print(len(all_products))
	json.dump(all_products, outfile)