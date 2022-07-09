import json
import os
import requests
from requests import ReadTimeout


def city_id(city: str, api_key: str) -> [int, str]:
    """Показывает destinationId для указанного города.
    Если нет в city_id_cash.json то делает запрос на city_id_cash.json и добавляет в city_id_cash.json.
    При отсутствии данных о городе присваивает значение: 'Ошибка: нет информации о городе'"""
    try:
        city: str = city.lower()
        with open(os.path.join('functions', '../logs/city_id_cash.json'), 'r', encoding='utf-8', ) as file:
            data = json.load(file)

        if city not in data.keys():
            url = "https://hotels4.p.rapidapi.com/locations/v2/search"
            querystring = {"query": city, "locale": "en_US", "currency": "RUB"}
            headers = {
                'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': api_key
            }
            response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
            data_api = json.loads(response.text)
            data[city] = int(data_api["suggestions"][0]["entities"][0]["destinationId"])
            with open(os.path.join('functions', '../logs/city_id_cash.json'), 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        my_city_id = data[city]
        return my_city_id
    except IndexError:
        return 'Ошибка: нет информации о городе'
    except ReadTimeout:
        return 'Ошибка: сервер не отвечает'
    except Exception as ex:
        return f'Ошибка: {ex}'
