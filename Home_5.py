from selenium import webdriver
import time
from pprint import pprint
import requests
from pymongo import MongoClient
from lxml.html import fromstring

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

client = MongoClient('localhost', 27017)
db = client["vk_posts"]
vk_collection = db.vk_posts

DRIVER_PATH = "./chromedriver"
url = 'https://vk.com/tokyofashion/'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(url)


ITEMS_XPATH = '//div[contains(@class, "withPostBottomAction")]'
DATE_XPATH = './/a[contains(@class, "post_link")]/span//text()'
TEXT_XPATH = './/div[contains(@class, "wall_post_text")]//text()'
HREF_XPATH = './/a[contains(@class, "post_link")]/@href'
LIKE_XPATH = './/span[contains(@class, "_counter_anim_container")]/div//text()'
SHARE_XPATH = './/div[contains(@class, "_share")]/span[contains(@class, "_counter_anim_container")]//text()'
LOOK_XPATH = './/div[contains(@class, "_views")]//text()'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}


def scrolling(PAGE_NUMBER):
    for i in range(PAGE_NUMBER):
        try:
            auth_popup = driver.find_element_by_class_name('UnauthActionBox__close').click()
            time.sleep(2)
        except:
            pass
        time.sleep(3)
        posts = driver.find_elements_by_class_name("post--with-likes")
        if not posts:
            break
        actions = ActionChains(driver)
        actions.move_to_element(posts[-1])
        actions.perform()
        html = driver.page_source
        print()


def vk_posts():
    response = requests.get(url, headers=HEADERS)
    dom = fromstring(response.text)
    items = dom.xpath(ITEMS_XPATH)
    info_list = []
    for item in items:
        info = {}
        info['date'] = item.xpath(DATE_XPATH)
        info['text'] = item.xpath(TEXT_XPATH)
        info['href'] = item.xpath(HREF_XPATH)[0]
        info['like'] = item.xpath(LIKE_XPATH)
        info['share'] = item.xpath(SHARE_XPATH)
        info['look'] = item.xpath(LOOK_XPATH)
        info_list.append(info)
        vk_collection.insert_one(info)
        pprint(info_list)


scrolling(3)
vk_posts()
driver.quit()