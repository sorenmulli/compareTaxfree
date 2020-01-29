import requests 
import json

import itertools


import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def floatify(string):
	return float((string.replace(".", "")).replace(",", "."))



def analyze_unit(prod, measurements):
	info_text = prod["name"]
	
	pant = False
	if " + pant"  in info_text:
		pant = True
		info_text = info_text.replace(" + pant", "")
	if " + Pant"  in info_text:
		pant = True
		info_text = info_text.replace(" + Pant", "")

	info_list = info_text.split(" ")
	
	measure = 0
	for m in measurements:
		if m in info_list:
			assert measure == 0
			measure = m
			measure_idx = info_list.index(measure)
	
	if measure != 0:
		#specialtilfælde
		if 'x' in info_list:
			x_idx = info_list.index('x')
			amount_text = ''.join(info_list[x_idx - 1: x_idx +2])
		else:
			amount_text = info_list[measure_idx-1] 
		
		print(info_text, amount_text)

		name = info_text.replace(measure, '').replace(amount_text, '')

		if 'x' in amount_text:
			a_list = amount_text.split('x')
			
			amount = int(a_list[0])
			size = floatify(a_list[1])
		else:
			filtered = itertools.filterfalse(str.isalpha, amount_text)
			amount_text = ''.join(list(filtered))

			amount = 1
			size = floatify(amount_text)


		size *= measurements[measure]
		measure = 'cl'
	else:
		amount = None
		size = None
		measure = ""

		name = info_text

	unit_info = {
			"u_amount": amount,
			"u_size": size,
			"u_measure": measure
		}
	
	name = name.strip()

	return name, unit_info, pant


scrape_url = "https://www.fleggaard.dk/Services/ProductService.asmx/ProductList?v=1.0&lId=0&so=7&cId=54&langId=1&countryId=11&locId=14917&customerId=0&mId={0}&p=1&rp=1000"

categories = {
	40373: 'ol',
	40385: 'vand',
	40514: 'cider',
	40406: 'vin',
	40391: 'spiritus'
}
all_products = list()

measurements = {'l.': 100, 'ml.': 0.1, 'cl.': 1}

for cat, cat_name in categories.items():
	r = requests.get(scrape_url.format(cat)).json()
	
	prods = r["data"]["items"]
	clean_prods = list()
	
	for prod in prods:
		clean_prod = {}
		clean_prod["original_name"] = prod["name"]
		clean_prod["price"] = [[price["quantity"], price["totalTagPriceIncVATAmount"]] for price in prod["salesPrices"]]
		clean_prod["category"] = cat_name
		clean_prod["name"], clean_prod["unit_info"], clean_prod["pant"] = analyze_unit(prod, measurements)
		clean_prods.append(clean_prod)
	all_products += clean_prods
		
	print(len(all_products))
with open("raw_fleggaard_prices.json", 'w+') as outfile:
	json.dump(all_products, outfile)