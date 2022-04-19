import requests
from pprint import pprint

cityname = input(f"Введите название города: ")
appid = '33a6d1a7554eb4daec73d45b73ed2987'
params = {'q': cityname,
          'appid': appid}


def weather_city(params):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url, params=params)
    j_data = response.json()
    return pprint(f"В городе {j_data['name']} температура {round(j_data['main']['temp'] - 273.15, 1)} градусов")


weather_city(params)