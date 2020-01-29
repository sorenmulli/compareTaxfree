import json, requests
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def floatify(string):
	return float((string.replace(".", "")).replace(",", "."))

def analyze_discount(prod):
	price_list = list()
	print(prod["price"]["amount"])
	std_price =	 floatify(prod["price"]["amount"])

	if "discount" in prod:
		disc_txt = prod["discount"]["discountText"]		
		
		#'Køb' medfører, at det er et mængdetilbud
		if "Køb" in disc_txt:
			
			
			single_info =  prod["unitPriceText2"]
			price_start = single_info.rfind(": ")
			price_end = single_info.find(" DKK")
			single_price = floatify(single_info[price_start+2:price_end])

			price_list.append([1, single_price])

			amount_start = disc_txt.rfind("Køb ")
			amount_end = disc_txt.find(" for")
			amount = disc_txt[amount_start+4:amount_end]

			price_list.append([int(amount), std_price])

	else:
		disc_txt = ""
		price_list.append([1, std_price])
	
	return price_list, disc_txt

def analyze_unit(prod):
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
	unit_info["u_size"] = floatify(size_list[0])
	unit_info["u_measure"] = size_list[1]


	return unit_info 


scrape_url = "https://www.bordershop.com/dk/bordershop/api/catalogsearchapi/productsearch?categoryId={0}&count=1000"

categories = {
	18: ['vin', 'rodvin', 'frankrig'], 17: ['vin', 'rodvin', 'spanien'], 9: ['spiritus', 'bitter'], 16: ['vin', 'rodvin', 'usa'], 8: ['vin', 'rose', 'spanien'], 19: ['vin', 'hvidvin', 'usa'], 4845: ['vand', 'sodavand'], 4847: ['vand', 'energidrik'],  4846: ['vand', 'kakao'], 4844: ['vand', 'sodavand'], 9793: ['vin', 'hedvin', 'portvin'], 9806: ['spiritus', 'cognac'], 9797: ['hedvin', 'vermouth'], 9801: ['spiritus', 'absinth'], 9791: ['vin', 'champagne-mousserende'], 9821: ['cider', 'cider'], 9820: ['ol-cider', 'alkoholfri'], 9805: ['spiritus', 'calvados'], 9803: ['spiritus', 'bitter'], 9810: ['spiritus', 'rom'], 9811: ['spiritus', 'shots'], 9792: ['spiritus', 'hedvin', 'vermouth'], 9813: ['spiritus', 'vodka'], 9818: ['ol', 'svensk-ol'], 9804: ['spiritus', 'brandy-armagnac'], 9802: ['spiritus', 'akvavit-snaps'], 9809: ['spiritus', 'ready-to-drink'], 9819: ['ol', 'special-ol'], 9814: ['spiritus', 'whisky', 'skotland'],9789: ['vin', 'rose', 'spanien'], 9807: ['spiritus', 'likor'], 9816: ['ol', 'special-ol'], 9812: ['spiritus', 'tequila'], 9808: ['spiritus', 'gin'], 9817: ['ol', 'dansk-ol']
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
		clean_prod["category"] = cat_name[0]
		clean_prod["category_detail"] = cat_name


		clean_prod["price"], clean_prod["discount_text"] = analyze_discount(prod)
		clean_prod["unit_info"] = analyze_unit(prod)

		clean_prods.append(clean_prod)
		raise ArithmeticError

	all_products += clean_prods
	print(len(all_products))
with open("raw_bordershop_prices.json", 'w+') as outfile:
	json.dump(all_products, outfile)

#print(prod_names)

