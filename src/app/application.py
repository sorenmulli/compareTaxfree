from flask import Flask, render_template, request
import product_loader

app = Flask(__name__)


@app.route("/")
def homepage():
    products = product_loader.load_products()
    length = len(products)
    product_names = [x["catagory"][0]["id"] for x in products]
    # products[0]["catagory"][0]["id"]

    return render_template("index.html",
                           products=products,
                           len=length,
                           product_ids=product_names)


@app.route("/products", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        product_id = request.form
        return render_template("category_page.html", product_id=product_id)



if __name__ == "__main__":
    app.run(debug=True)
