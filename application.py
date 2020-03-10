from flask import Flask, render_template, request
from app.AppModules import product_loader

app = Flask(__name__)

db = product_loader.load_products()
product_ids = list(db.keys())
best_value = product_loader.find_best_value(db, 10)


@app.route("/")
def homepage():
    length = len(db)

    return render_template("index.html",
                           product_ids=product_ids,
                           best_value=best_value)


@app.route("/products", methods=["GET", "POST"])
def product():
    if request.method == "POST":
        product_id = request.form["prodID"]
        return render_template("category_page.html",
                               product_id=product_id,
                               products=db[product_id],
                               product_ids=product_ids)


if __name__ == "__main__":
    app.run(debug=True)
