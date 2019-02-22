import requests
import pymongo

import sys
import re

from bs4 import BeautifulSoup


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.dialog_system

propertyList = {"price": True}
brandList = {}


def scrapeDataForItem(url, category):
    product = {}
    # print url
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "lxml")
        keys = soup.find_all("td", {"class": "_3-wDH3 col col-3-12"})
        vals = soup.find_all("td", {"class": "_2k4JXJ col col-9-12"})

        i = 0
        j = 0
    data = {}
    while j < len(vals) and i < len(keys):

      #  print(keys[j].text)
        data[keys[j].text] = vals[j].text
      #  print(vals[j].text)
        j += 1
        i += 1
    db[category].insert_one(data)
    print(data)
    '''
        while j < len(vals) and i < len(keys):
            if (vals[j].get("colspan")):
                j += 1
            else:
                prop = keys[i].text.encode('utf-8').strip('\t\r\n ').lower()
                if prop.find(".") == -1:
                    propertyList[prop] = True
                    product[prop] = vals[j].text.encode('utf-8').strip('\t\r\n ').lower()
                    if prop.lower() == "brand":
                        brandList[product[prop]] = True
                    i += 1
                    j += 1
                else:
                    i += 1

        price = BeautifulSoup(r.content, "lxml").find_all("span", {"class": "selling-price omniture-field"})

        try:
            tmp = product["model name"]
        except KeyError:
            try:
                product["model name"] = product["model id"]
            except KeyError:
                return

        try:
            product["_id"] = product["model name"]
            product["price"] = price[0].text.encode('utf-8').strip('\t\r\n ').lower()
           # db[category].insert_one(product)
            print(product["_id"], category)
        except IndexError:
            print("[[No Price]]: " + product["_id"], category)
    '''

#  ==========================      SPIDER FOR GOING THROUGH ALL THE LINKS
def StartSpider():
    categories = {"mobiles": "tyy,4io"}
    LeftPartUrl = "https://www.flipkart.com/"
    Middle = "/pr?sid="
    MiddlePart1Url = "&filterNone=true&start="
    RightPartUrl = "&ajax=true&_=1458931757008"

    for key in categories:
        category = categories[key]
        start = 1
        url = LeftPartUrl + key + Middle + category + MiddlePart1Url + str(start) + RightPartUrl
        # print url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml").find_all("div", {"class":"_3gm0O6"})
        while r.status_code == 200:
            for item in soup:
                if(item.find_all("a")):
                    print(item.text)
                    url = LeftPartUrl[:-1] + item.find_all("a")[0].get("href")
                    scrapeDataForItem(url, key)
            start += 20
            url = LeftPartUrl + category + MiddlePart1Url + str(start) + RightPartUrl
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml").find_all("div", {"class": "pu-title fk-font-13"})
        for item in soup:
            url = LeftPartUrl +  item.find_all("a")[0].get("href")
            scrapeDataForItem(url, key)



StartSpider()
#fptr.close()
#brandptr.close()