import sys, os
import json
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'PyUtils'))
from  pyutils import alphabetize

from difflib import SequenceMatcher

class Merger:
	def __init__(self, raw_db: dict = None):
		self.raw_db = raw_db
		self.clean_db = {}
		self.categori_translation = {
			'spiritus': ['spiritus', 'hedvin'],
			'vin': ['vin', 'hedvin'],
			'ol': ['ol', 'ol-cider'],
			'cider': ['cider', 'ol_cider']
		#	'ol-cider': ['ol', 'cider']
		}
		

	def db_from_json_file(self, path):
		with open(path, 'r') as infile:
			self.raw_db = json.load(infile)

	def merge_dbs(self):

		for dk_item in self.raw_db['dk']:
			fleg_item = self.best_match(dk_item, self.raw_db['fleg'])
			border_item = self.best_match(dk_item, self.raw_db['border'])
			
			self.merge_items(dk_item, fleg_item, border_item)
			

	def merge_items(self, dk: dict, fleg: dict, border: dict):
		if not (fleg is None and border is None):
			clean_unit = {}
			if fleg is None:
				clean_unit["fleg_price"] = None
				clean_unit["fleg_unit_info"] = None

			else:
				clean_unit["fleg_price"] = fleg["price"]
				clean_unit["fleg_unit_info"] = fleg["unit_info"]


			if border is None:
				clean_unit["category_detail"] = None

				clean_unit["border_price"] = None
				clean_unit["border_unit_info"] = None

			else:

				clean_unit["category_detail"] = border["category_detail"] 

				clean_unit["border_price"] = border["price"]
				clean_unit["border_unit_info"] = border["unit_info"]
			clean_unit["category"] = dk["category"]
			clean_unit["name"] = dk["name"]
			clean_unit["dk_price"] = dk["price"]
			print("\nPRODUCT\n")
			print(dk["name"])
			
			if border is not None: print(border["name"], SequenceMatcher(None, border["name"].lower(), dk["name"].lower()).ratio() ) 
			if fleg is not None: print(fleg["name"], SequenceMatcher(None, fleg["name"].lower(), dk["name"].lower()).ratio() ) 
			
			if clean_unit["category"] not in self.clean_db.keys():
				self.clean_db[clean_unit["category"]] = [clean_unit]
			else:
				self.clean_db[clean_unit["category"]].append(clean_unit)

	def best_match(self, dk_item: dict, db: dict):		
		N = len(db)
		scores = np.empty(N)
		for i, item in enumerate(db):
			scores[i] = self.score(dk_item, item)
		if scores.max() >= 45:
			return db[scores.argmax()]
		else: 
			return None

	def score(self, dk_item: dict, item: dict):
		score = 0
		
		if item["category"] in self.categori_translation[ dk_item["category"] ]:
			score += 25
		if item["name"] in dk_item["name"]:
			score += 50
		if alphabetize(item["name"]) in dk_item["name"]:
			score += 50
		match = SequenceMatcher( None, item["name"].lower(), dk_item["name"].lower() ).ratio()
		score += match * 25 
		


		dk_price, item_price = self.get_singleprice(dk_item), self.get_singleprice(item)
		if item_price >= dk_price*0.5 and item_price <= dk_price*1.5:
			score += 10 
		
		return score


	def get_singleprice(self, item: dict):
		price_dict = item["price"]
		if "1" in price_dict.keys():
			return price_dict["1"]
		else: 
			quant = min( price_dict.keys() )  
			return price_dict["quant"]/int(quant)
		



if __name__ == "__main__":
	m = Merger()
	m.db_from_json_file('src/modules/raw_db.json') #assume pwd is repo
	
	print(len(m.raw_db["dk"]))
	m.merge_dbs()
	print(sum
	(	[len(m.clean_db[cat]) for cat in m.clean_db.keys()] 	)
	)
	with open('src/clean_db.json', 'w+') as outfile:
		json.dump(m.clean_db, outfile)


#dk_categories = list()
#for item in dk_items:
#	dk_categories.append(item["category"])
#print(np.unique(dk_categories, return_counts = True))

#fleg_categories = list()
#for item in fleg_items:
#	fleg_categories.append(item["category"])
#print(np.unique(fleg_categories, return_counts = True))

#border_categories = list()
#for item in border_items:
#	border_categories.append(item["category"])

#print(np.unique(border_categories, return_counts = True))
