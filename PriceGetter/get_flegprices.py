import requests 
import json

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



scrape_url = "https://www.fleggaard.dk/Services/ProductService.asmx/ProductList?v=1.0&lId=0&so=7&cId=54&langId=1&countryId=11&locId=14917&customerId=0&mId={0}&p=1&rp=1000"

categories = [40385, 40514, 40406, 40373, 40391]

all_products = list()

for cat in categories:
	r = requests.get(scrape_url.format(cat)).json()
	
	prods = r["data"]["items"]
	clean_prods = list()
	
	for prod in prods:
		clean_prod = {}
		
		clean_prod["name"] = prod["name"]
		clean_prod["price"] = [[price["quantity"], price["totalTagPriceIncVATAmount"]] for price in prod["salesPrices"]]
		clean_prod["category"] = cat
					
		clean_prods.append(clean_prod)
	all_products += clean_prods
		
	print(len(all_products))
with open("fleggaard_prices.json", 'w+') as outfile:
	json.dump(all_products, outfile)