import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'PyUtils'))
from  pyutils import floatify_dk_num

import itertools
import requests 
import json




class Collector:
	def __init__(self):
		self.measurements = {'l.': 100, 'ml.': 0.1, 'cl.': 1}
	
	def update_raw(self, do_dk: bool = True, do_fleg: bool = True, do_border: bool = True):
		raw_db = {}
		if do_dk:
			print("[info]: Scraping dk prices")
			try:
				raw_db["dk"] = self.dk_requests()
			except Exception as e:
				print(e)

		if do_fleg:
			print("[info]: Scraping fleg prices")
			try:
				raw_db["fleg"] = self.fleg_requests()
			except Exception as e:
				print(e)

		if do_border:
			print("[info]: Scraping border prices")
			try:
				raw_db["border"] = self.border_requests()
			except Exception as e:
				print(e)

		return raw_db
 

	def dk_requests(self):
		'''
		Performs scrape of danish prices
		'''

		scrape_url = "https://butik.mad.coop.dk/api/search/search?categories={0}&lastFacet=categories&pageSize=10000"

		all_products = list()

		categories = {
			"ol": 426,
			"ol": 431,
			"cider": 432,
			"spiritus": 433,
			"vin": 307,
	#		"vand": 406
		}

		# Search is performed one category at a time 
		for cat, cat_id in categories.items():
			r = requests.get(scrape_url.format(cat_id)).json()
			
			prods = r["products"]
			if prods is None:
				break
			clean_prods = list()
			
			# Products are gathered and casted 
			for prod in prods:
				clean_prod = {}
				
				clean_prod["name"] = prod["spotText"]
				clean_prod["price"] = {1: float(prod["salesPrice"]["amount"])}
				
				clean_prod["category"] = cat
							
				clean_prods.append(clean_prod)
			all_products += clean_prods
					
		print(f"[info]: Number of scraped dk prices: {len(all_products)}")
		return all_products



	def fleg_requests(self):
		'''
		Performs scrape of Fleggaard
		'''
		scrape_url = "https://www.fleggaard.dk/Services/ProductService.asmx/ProductList?v=1.0&lId=0&so=7&cId=54&langId=1&countryId=11&locId=14917&customerId=0&mId={0}&p=1&rp=1000"

		categories = {
			40373: 'ol',
#			40385: 'vand',
			40514: 'cider',
			40406: 'vin',
			40391: 'spiritus'
		}
		all_products = list()

		for cat, cat_name in categories.items():
			r = requests.get(scrape_url.format(cat)).json()
			
			prods = r["data"]["items"]
			clean_prods = list()
			
			for prod in prods:
				clean_prod = {}
				clean_prod["original_name"] = prod["name"]
				clean_prod["price"] = {int(price["quantity"]): price["totalTagPriceIncVATAmount"] for price in prod["salesPrices"]}
				clean_prod["category"] = cat_name
				clean_prod["name"], clean_prod["unit_info"], clean_prod["pant"] = self._fleg_unit_analyzer(prod)
				clean_prods.append(clean_prod)
			all_products += clean_prods
				
		print(f"[info]: Number of scraped fleg prices: {len(all_products)}")

		return all_products

	def border_requests(self):
		'''
		Performs scrape of bordershop
		'''

		scrape_url = "https://www.bordershop.com/dk/bordershop/api/catalogsearchapi/productsearch?categoryId={0}&count=1000"

		categories = {
			18: ['vin', 'rodvin', 'frankrig'], 17: ['vin', 'rodvin', 'spanien'], 9: ['spiritus', 'bitter'], 16: ['vin', 'rodvin', 'usa'], 8: ['vin', 'rose', 'spanien'], 19: ['vin', 'hvidvin', 'usa'], 4845: ['vand', 'sodavand'], 4847: ['vand', 'energidrik'],  4846: ['vand', 'kakao'], 4844: ['vand', 'sodavand'], 9793: ['vin', 'hedvin', 'portvin'], 9806: ['spiritus', 'cognac'], 9797: ['hedvin', 'vermouth'], 9801: ['spiritus', 'absinth'], 9791: ['vin', 'champagne-mousserende'], 9821: ['cider', 'cider'], 9820: ['ol-cider', 'alkoholfri'], 9805: ['spiritus', 'calvados'], 9803: ['spiritus', 'bitter'], 9810: ['spiritus', 'rom'], 9811: ['spiritus', 'shots'], 9792: ['spiritus', 'hedvin', 'vermouth'], 9813: ['spiritus', 'vodka'], 9818: ['ol', 'svensk-ol'], 9804: ['spiritus', 'brandy-armagnac'], 9802: ['spiritus', 'akvavit-snaps'], 9809: ['spiritus', 'ready-to-drink'], 9819: ['ol', 'special-ol'], 9789: ['vin', 'rose', 'spanien'], 9807: ['spiritus', 'likor'], 9816: ['ol', 'special-ol'], 9812: ['spiritus', 'tequila'], 9808: ['spiritus', 'gin'], 9817: ['ol', 'dansk-ol']
		}
		#9814: ['spiritus', 'whisky', 'skotland'],
		all_products = list()
		for cat, cat_name in categories.items():
	#		print(cat, cat_name)
			r = requests.get(scrape_url.format(cat)).json()
			
			prods = r["products"]
			clean_prods = list()

			for prod in prods:
				clean_prod = {}
				
				clean_prod["name"] = prod["displayName"]
				clean_prod["category"] = cat_name[0]
				clean_prod["category_detail"] = cat_name


				clean_prod["price"], clean_prod["discount_text"] = self._border_discount_analyzer(prod)
				
				if not clean_prod["price"]:
					continue
				
				clean_prod["unit_info"] = self._border_unit_analyzer(prod)

				clean_prods.append(clean_prod)

			all_products += clean_prods
		print(f"[info]: Number of scraped border prices: {len(all_products)}")
		return all_products
	def _fleg_unit_analyzer(self, prod: dict):
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
		for m in self.measurements:
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
			
	#		print(info_text, amount_text)

			name = info_text.replace(measure, '').replace(amount_text, '')

			if 'x' in amount_text:
				a_list = amount_text.split('x')
				
				amount = int(a_list[0])
				size = floatify_dk_num(a_list[1])
			else:
				filtered = itertools.filterfalse(str.isalpha, amount_text)
				amount_text = ''.join(list(filtered))

				amount = 1
				size = floatify_dk_num(amount_text)


			size *= self.measurements[measure]
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

	

	def _border_unit_analyzer(self, prod: dict):
		unit_info = {
				"u_name": prod["uom"], 
				}
		unit_text  = prod["unitPriceText1"]
		
		if '×' in unit_text:
			u_list = unit_text.split(' × ')
			unit_amount = u_list[0]
			unit_size_text = u_list[1]

		else:
			unit_amount = 1
			unit_size_text = unit_text
		unit_info["u_amount"] = unit_amount

		size_list = unit_size_text.split(' ')
		unit_info["u_size"] = floatify_dk_num(size_list[0])
		unit_info["u_measure"] = size_list[1]


		return unit_info 

	def _border_discount_analyzer(self, prod: dict):

		price_dict = dict()
		#print(prod["price"]["amount"])
		std_price =	 floatify_dk_num(prod["price"]["amount"])

		if "discount" in prod:
			disc_txt = prod["discount"]["discountText"]		
			
			#'Køb' medfører, at det er et mængdetilbud
			if "Køb" in disc_txt:
				
				
				single_info =  prod["unitPriceText2"]
				price_start = single_info.rfind(": ")
				price_end = single_info.find(" DKK")
				single_price = floatify_dk_num(single_info[price_start+2:price_end])

				price_dict[1] =  single_price

				amount_start = disc_txt.rfind("Køb ")
				amount_end = disc_txt.find(" for")
				amount = disc_txt[amount_start+4:amount_end]

				price_dict[int(amount)] = std_price

		else:
			disc_txt = ""
			price_dict[1]= std_price
		
		return price_dict, disc_txt

if __name__ == "__main__":
	os.chdir(sys.path[0])
	c = Collector()
	db = c.update_raw()
	
	with open("../raw_db.json", 'w+') as outfile:
		json.dump(db, outfile)




# 	def dk_requests(self):
# '''
# Performs scrape of pricerunner.dk
# '''

# scrape_url = "https://www.pricerunner.dk/public/v1/cl/{0}/dk/desktop?page={1}&retailer=63022&urlName={2}&sort=1"

# all_products = list()

# categories = {
# 	"vin": 465,
# 	"OEl-og-spiritus": 1424,
# }
# cat_translate = {
# 	465: 'vin',
# 	1424: 'ol-spiritus-vand-cider'
# }

# # Search is performed one category at a time 
# for cat, cat_id in categories.items():
# 	for i in range(1, 10000):
# 		r = requests.get(scrape_url.format(cat_id, i, cat)).json()
		
# 		prods = r["viewData"]["category"]["products"]
# 		if prods is None:
# 			break
# 		clean_prods = list()
		
# 		# Products are gathered and casted 
# 		for prod in prods:
# 			clean_prod = {}
			
# 			clean_prod["name"] = prod["name"]
# 			clean_prod["price"] = {1: float(prod["localMinPrice"]["value"])}
# 			clean_prod["category"] = cat_translate[cat_id]
						
# 			clean_prods.append(clean_prod)
# 		all_products += clean_prods
			
# print(f"[info]: Number of scraped dk prices: {len(all_products)}")
# return all_products
