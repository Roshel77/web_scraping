import requests
import json

url = 'https://api.github.com'
username = input(f"Введите имя пользователя: ")


def write_json(response):
    with open("data_repo.json", "w") as fw:
        for repo in response.json():
            json.dump(repo['name'], fw, indent=2)

def list_repo(response):
    for repo in response.json():
        print(f"Репозиторий: {repo['name']}")


response = requests.get(f'{url}/users/{username}/repos')
write_json(response)
list_repo(response)