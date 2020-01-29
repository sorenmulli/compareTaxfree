from json import loads

def load_products():
    path = "static/ComparedPrices.json"
    with open(path, "r") as f:
        products = loads(f.read())
    return products
