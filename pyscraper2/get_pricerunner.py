import json 

with open("ex.json") as pricefile:
	
	products = data["viewData"]["category"]["products"]
	for prod in products:

		print(prod["localMinPrice"]["value"])
		print(prod["name"], "\n")

		print(i)
		i+=1
#	print(prod[0])