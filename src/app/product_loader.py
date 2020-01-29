from json import loads


def load_products():
    path = "static/clean_db.json"
    with open(path, "r") as f:
        products = loads(f.read())
    return products

if __name__ == "__main__":
    print(load_products())