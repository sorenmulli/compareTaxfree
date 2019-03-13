import json, requests
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



scrape_url = "https://www.bordershop.com/dk/bordershop/api/catalogsearchapi/productsearch?categoryId={0}&count=1000"

categories = {
	18: 'vin/rodvin/frankrig', 17: 'vin/rodvin/spanien', 9: 'spiritus/bitter', 16: 'vin/rodvin/usa', 8: 'vin/rose/spanien', 19: 'vin/hvidvin/usa', 4845: 'vand/sodavand', 4847: 'vand/energidrik', 4850: 'slik-snacks/chokolade', 4846: 'vand/kakao', 4844: 'vand/sodavand', 9793: 'vin/hedvin/portvin', 9806: 'spiritus/cognac', 9797: 'hedvin/vermouth', 9801: 'spiritus/absinth', 9791: 'vin/champagne-mousserende', 9821: 'ol-cider/cider', 9820: 'ol-cider/alkoholfri', 9805: 'spiritus/calvados', 9803: 'spiritus/bitter', 9810: 'spiritus/rom', 9811: 'spiritus/shots', 9792: 'spiritus/hedvin/vermouth', 9813: 'spiritus/vodka', 9818: 'ol-cider/svensk-ol', 9804: 'spiritus/brandy-armagnac', 9802: 'spiritus/akvavit-snaps', 9809: 'spiritus/ready-to-drink', 9819: 'ol-cider/special-ol', 9814: 'spiritus/whisky/skotland',9789: 'vin/rose/spanien', 9807: 'spiritus/likor', 9816: 'ol-cider/special-ol', 9812: 'spiritus/tequila', 9808: 'spiritus/gin', 9817: 'ol-cider/dansk-ol'
}

all_products = list()

#prod_names = {}

for cat, cat_name in categories.items():
	r = requests.get(scrape_url.format(cat)).json()
	
	prods = r["products"]
	clean_prods = list()

#	cat_url = prods[0]['url']
#	end_idx = cat_url.rfind('/')
#	prod_names[cat] = cat_url[0:end_idx]

	for prod in prods:
		clean_prod = {}
		
		clean_prod["name"] = prod["displayName"]
		clean_prod["category"] = cat_name

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

#print(prod_names)