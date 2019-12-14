from flask import Flask

from scraping_by import PRODUCTS, scrape

app = Flask(__name__)


@app.route("/")
def hello():
    return "🤑 Hello"


@app.route("/scrape")
def scrape_products():
    return scrape(PRODUCTS)


if __name__ == "__main__":
    app.run()
