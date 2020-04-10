import locale
from os import environ
from random import randint
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()

locale.setlocale(locale.LC_ALL, "")

API_URL = "https://www.woolworths.com.au/apis/ui/product/detail/{}?isMobile=false"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:71.0) Gecko/20100101 Firefox/71.0"
}

PRODUCTS = [
    922828,  # Dorset cereals nut granola
    609558,  # Dorset cereals berry granola
    575838,  # Mayvers dark crunchy peanut butter
    781034,  # Mayvers regular crunchy peanut butter
    49905,  # Bonne Maman raspberry jam
    269903,  # Barker's Anathoth raspberry jam
    227264,  # Earth Choice dish soap
]


def getProductData(productId):
    response = requests.get(API_URL.format(str(productId)), headers=HEADERS)
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


errorMessages = []

for product in PRODUCTS:
    productData = getProductData(product)
    sleep(randint(10, 20))
    if productData and getCurrentPrice(productData):
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
        errorMessages.append(message)

if len(errorMessages) > 0:
    message = "\n".join(errorMessages)
    postToSlack("\n" + message)
