from flask import Flask

from scraping_by import PRODUCTS, composeAndPostMessage, scrape

app = Flask(__name__)


@app.route("/")
def hello():
    return "🤑 Hello"


@app.route("/scrape")
def scrape_all():
    return scrape(PRODUCTS)


@app.route("/scrape/<id_>")
def scrape_by_id(id_):
    try:
        index = PRODUCTS.index(int(id_))
        print(index)
        product = PRODUCTS[index]
        composeAndPostMessage(product)
        return "🤑 Scraped product {}".format(product)
    except Exception as e:
        return "🤑" + str(e)


if __name__ == "__main__":
    app.run()
