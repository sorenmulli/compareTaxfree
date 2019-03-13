import json, requests
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



scrape_url = "https://www.bordershop.com/dk/bordershop/api/catalogsearchapi/productsearch?categoryId={0}&count=1000"

categories = ['18', '17', '9', '16', '8', '19', '4845', '4847', '4850', '4846', '4844', '9793', '9806', '9797', '9801', '9791', '9821', '9820', '9805', '9803', '9810', '9811', '9792', '9813', '9818', '9804', '9802', '9809', '9819', '9814', '9789', '9807', '9816', '9812', '9808', '9817']

all_products = list()

for cat in categories:
	r = requests.get(scrape_url.format(cat)).json()
	
	prods = r["products"]
	clean_prods = list()
	
	for prod in prods:
		clean_prod = {}
		
		clean_prod["name"] = prod["displayName"]
		clean_prod["category"] = cat

		if "discount" in prod:
			clean_prod["discount_text"] = prod["discount"]["discountText"]
		else:
			clean_prod["discount_text"] = ""
		clean_prod["unit_info"] = {
			"unit_name:": prod["uom"], 
			"unit_size:": prod["unitPriceText1"],
			"unit_price": prod["unitPriceText2"]
			}
		
		clean_prod["price"] = prod["price"]["amount"].replace(",", ".")
		
		clean_prods.append(clean_prod)
		
		
	all_products += clean_prods
		
	print(len(all_products))
with open("raw_bordershop_prices.json", 'w+') as outfile:
	json.dump(all_products, outfile)