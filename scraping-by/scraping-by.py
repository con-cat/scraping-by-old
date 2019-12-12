import json
import urllib.request
import locale

locale.setlocale(locale.LC_ALL, "")

API_URL = "https://www.woolworths.com.au/apis/ui/product/detail/{}?isMobile=false"

PRODUCTS = [
    922828,  # Dorset cereals nut granola
    609558,  # Dorset cereals berry granola
    575838,  # Mayvers dark crunchy peanut butter
    781034,  # Mayvers regular crunchy peanut butter
    360257,  # Pic's crunchy peanut butter
]


def getProductData(productId):
    response = urllib.request.urlopen(API_URL.format(str(productId)))
    return json.load(response)["Product"]


def getName(product):
    return product["Name"].strip()


def isOnSpecial(product):
    return product["InstoreIsOnSpecial"]


def getCurrentPrice(product):
    return product["InstorePrice"]


def getDiscount(product):
    return product["InstoreSavingsAmount"] / product["InstoreWasPrice"]


for product in PRODUCTS:
    productData = getProductData(product)
    name = getName(productData)
    currentPrice = locale.currency(getCurrentPrice(productData))
    if isOnSpecial(productData):
        discount = "{0:.0%}".format(getDiscount(productData))
        print(
            "🚨🤑 {name} is on special!!!! Current price: {currentPrice}, {discount} discount!".format(
                name=name, currentPrice=currentPrice, discount=discount
            )
        )
    else:
        print(
            "👎💸 {name} is not on special. Current price: {currentPrice}".format(
                name=name, currentPrice=currentPrice
            )
        )
