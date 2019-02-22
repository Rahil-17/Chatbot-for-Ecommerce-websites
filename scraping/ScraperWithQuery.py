import requests
import pymongo

import sys
import re

from bs4 import BeautifulSoup
from queryHandlerModified import *

client = pymongo.MongoClient('mongodb://user:password123@ds123963.mlab.com:23963/project', connectTimeoutMS=300000)
db = client.get_default_database()
flipkart_data = db.flipkart_data

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
        data[keys[j].text.lower()] = vals[j].text.lower()
      #  print(vals[j].text)
        j += 1
        i += 1
    flipkart_data.insert_one(data)
    result = flipkart_data.find_one({"model name":data["model name"]})
    print(result)
    

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


def chatWithUser():
    query = input()
    print(getProductUsingCompare(query))
StartSpider()
#fptr.close()
#brandptr.close()
