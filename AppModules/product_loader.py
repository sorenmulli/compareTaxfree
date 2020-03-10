from json import loads


def load_products():
    path = "static/clean_db.json"
    with open(path, "r") as f:
        products = loads(f.read())
    return products


def find_best_value(jsonfile, num_of_products):
    value_dict = {}
    def price_dif(product):

        fleg_dif = -99999
        border_dif = -99999
        if product["fleg_price"] is not None:
            fleg_dif = product["dk_price"]["1"] - product["fleg_price"]["1"]
        if product["border_price"] is not None:
            border_dif = product["dk_price"]["1"] - product["border_price"]["1"]


        if fleg_dif == -99999 and border_dif == -99999:
            pass
        elif fleg_dif > border_dif:
            best_value = fleg_dif
        else:
            best_value = border_dif

        value_dict[best_value] = product

    for product_category in jsonfile.values():
        for product in product_category:
            price_dif(product)

    best_value = list(sorted(value_dict.items(), reverse=True))[0:num_of_products]
    return [x[1] for x in best_value]

if __name__ == "__main__":
    json_file = load_products()
    products =  find_best_value(json_file, 3)