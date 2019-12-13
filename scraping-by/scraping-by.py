import json
import locale
from os import environ

import requests

locale.setlocale(locale.LC_ALL, "")

API_URL = "https://www.woolworths.com.au/apis/ui/product/detail/{}?isMobile=false"

PRODUCTS = [
    922828,  # Dorset cereals nut granola
    609558,  # Dorset cereals berry granola
    575838,  # Mayvers dark crunchy peanut butter
    781034,  # Mayvers regular crunchy peanut butter
    49905,   # Bonne Maman raspberry jam
    269903,  # Barker's Anathoth raspberry jam
    227264,  # Earth Choice dish soap
]


def getProductData(productId):
    response = requests.get(API_URL.format(str(productId)))
    if response.status_code == 200:
        return response.json()["Product"]
    else:
        return None


def getName(product):
    return product["Name"].strip()


def isOnSpecial(product):
    return product["InstoreIsOnSpecial"]


def getCurrentPrice(product):
    return product["InstorePrice"]


def getDiscount(product):
    return product["InstoreSavingsAmount"] / product["InstoreWasPrice"]


def postToSlack(message):
    if environ.get("SLACK_URL"):
         return requests.post(environ["SLACK_URL"], json={"text": "<!here> " + message},)
    else:
        print("⚠️ Didn't post to Slack")


for product in PRODUCTS:
    productData = getProductData(product)
    if productData:
        name = getName(productData)
        currentPrice = locale.currency(getCurrentPrice(productData))
        if isOnSpecial(productData):
            discount = "{0:.0%}".format(getDiscount(productData))
            message = "🚨🤑 {name} is on special!!!! Current price: {currentPrice}, {discount} discount!".format(
                name=name, currentPrice=currentPrice, discount=discount
            )
            print(message)
            postToSlack(message)
        else:
            print(
                "👎💸 {name} is not on special. Current price: {currentPrice}".format(
                    name=name, currentPrice=currentPrice
                )
            )
    else:
        message = "💔🙁 Can't find product id {}".format(str(product))
        print(message)
        postToSlack(message)
