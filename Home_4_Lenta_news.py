from pprint import pprint
import requests
from pymongo import MongoClient
from lxml.html import fromstring

client = MongoClient('localhost', 27017)
db = client["news"]
news_collection = db.news


def get_first_elem_or_none(arr):
    if arr:
        return arr[0]
    return None


URL_Lenta = "https://lenta.ru/parts/news/"
ITEMS_XPATH_Lenta = '//ul[contains(@class, "__body")]/li'
TITLE_XPATH_Lenta = './/*[contains(@class, "news__title")]//text()'
DATE_XPATH_Lenta = './/*[contains(@class, "news__date")]//text()'
HREF_XPATH_Lenta = './/a/@href'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

response_lenta = requests.get(URL_Lenta, headers=HEADERS)
dom_lenta = fromstring(response_lenta.text)
items_lenta = dom_lenta.xpath(ITEMS_XPATH_Lenta)
info_list_lenta = []

def lenta_news():
    response_lenta = requests.get(URL_Lenta, headers=HEADERS)
    dom_lenta = fromstring(response_lenta.text)
    items_lenta = dom_lenta.xpath(ITEMS_XPATH_Lenta)
    info_list_lenta = []

    for item_lenta in items_lenta:
        info_lenta = {}
        info_lenta['source'] = URL_Lenta
        info_lenta["title"] = get_first_elem_or_none(item_lenta.xpath(TITLE_XPATH_Lenta))
        info_lenta["date"] = item_lenta.xpath(DATE_XPATH_Lenta)
        info_lenta["href"] = get_first_elem_or_none(item_lenta.xpath(HREF_XPATH_Lenta))
        if info_lenta["title"] is not None:
            info_list_lenta.append(info_lenta)
        #     news_collection.insert_one(info_lenta)  # Сохраняем данные в БД


    pprint(info_list_lenta)

lenta_news()