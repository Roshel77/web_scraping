from pprint import pprint
import requests
from pymongo import MongoClient
from lxml.html import fromstring

client = MongoClient('localhost', 27017)
db = client["news"]
news_collection = db.news


def get_value(link, xpath):
    response = requests.get(link, headers=HEADERS)
    dom = fromstring(response.text)
    value = dom.xpath(xpath)
    return value


URL_Yandex = 'https://yandex.ru/news/'
ITEMS_XPATH_Yandex = '//div[contains(@class, "news-top-flexible-stories")]/div'
TITLE_XPATH_Yandex = './/a[contains(@class, "mg-card__link")]//text()'
HREF_XPATH_Yandex = './/a[contains(@class, "mg-card__link")]/@href'
SOURCE_XPATH_Yandex = '//article//span[contains(@class, "news-story__subtitle-text")]//text()'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

response_yandex = requests.get(URL_Yandex, headers=HEADERS)
dom_yandex = fromstring(response_yandex.text)
item_yandex = dom_yandex.xpath(ITEMS_XPATH_Yandex)
info_list_yandex = []


def news_Yandex():
    for item_yandex in items_yandex:
        info_yandex = {}
        info_yandex['title'] = item_yandex.xpath(TITLE_XPATH_Yandex)
        link_news = item_yandex.xpath(HREF_XPATH_Yandex)[0]
        info_yandex["href"] = link_news
        info_yandex['source'] = get_value(link_news, SOURCE_XPATH_Yandex)
        info_list_yandex.append(info_yandex)

    pprint(info_list_yandex)


news_Yandex()