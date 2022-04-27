from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint
from pymongo import MongoClient
import re


def hh_job():
    client = MongoClient('localhost', 27017)
    db = client["positions"]
    collection = db.all_positions

    position = input('Введите должность: ')
    num_page = int(input('Введите количество страниц: '))
    url = 'https://hh.ru/search/vacancy'
    params = {'clusters': 'name',
              'ored_clusters': 'true',
              'salary': '',
              'text': position,
              'page': 0,
              'hhtmFrom': 'vacancy_search_list'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    position_list = []

    for i in range(num_page):
        pos = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for el in pos:
            position_data = {}
            count_position = 0
            info = el.find('a', {'class': 'bloko-link'})
            href = info['href'].split('?')[0]
            job_id = href.split('/')[-1]
            name = info.text
            link_vacancy = el.find('span', {'class': 'g-user-content'}).find('a').get('href')
            price_job = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            if price_job is None:
                price_job_min = price_job_max = currency = 'None'
            else:
                job_price = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                currency = job_price[-1]
                if len(job_price) == 3:
                    price_job_min = price_job_max = job_price[1]

                else:
                    price_job_min, price_job_max = job_price[0], job_price[2]

            next_page = soup.find_all('span', {'class': 'bloko-button bloko-button_pressed'})
            if not next_page:
                break

            position_data['_id'] = job_id,
            position_data['name_job'] = name,
            position_data['link_vacancy'] = link_vacancy,
            position_data['price_job_min'] = price_job_min.replace('\u202f', ''),
            position_data['price_job_max'] = price_job_max.replace('\u202f', ''),
            position_data['currency'] = currency,
            position_data['website'] = url

            if not list(collection.find(position_data)):
                collection.insert_one(position_data)
                count_position += 1

            position_list.append(position_data)

    # pprint(position_list)

    return position_list


hh_job()