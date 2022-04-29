
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


URL_Mail = 'https://news.mail.ru/'
ITEMS_XPATH_Mail = '//ul[contains(@class, "js-module")]//li'
TITLE_XPATH_Mail = './/a[contains(@class, "list__text")]//text()'
DATE_XPATH_Mail = './/span[contains(@class, "breadcrumbs__text")]/@datetime'
HREF_XPATH_Mail = './/a[contains(@class, "list__text")]/@href'
SOURCE_XPATH_Mail = '//a[contains(@class, "breadcrumbs__link")]/span//text()'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

response_mail = requests.get(URL_Mail, headers=HEADERS)
dom_mail = fromstring(response_mail.text)
items_mail = dom_mail.xpath(ITEMS_XPATH_Mail)
info_list_mail = []


def news_mail():
    for item_mail in items_mail:
        info_mail = {}
        info_mail['title'] = item_mail.xpath(TITLE_XPATH_Mail)
        link_news = item_mail.xpath(HREF_XPATH_Mail)[0]
        info_mail["href"] = link_news
        info_mail['source'] = get_value(link_news, SOURCE_XPATH_Mail)
        info_mail['date'] = get_value(link_news, DATE_XPATH_Mail)
        info_list_mail.append(info_mail)
    pprint(info_list_mail)


news_mail()