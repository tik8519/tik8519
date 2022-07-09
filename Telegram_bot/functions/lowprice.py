import json
import requests
from requests import ReadTimeout
from functions.bestdeal import data_reader


def lowprice(destination_id: int, api_key: str, check_in: str, check_out: str, sort_order: str,
             page_size: int = 25) -> list:
    """Делает запрос rapidapi.com в зависимости от значения 'sort_order' получает данные с упорядочеными по
     стоимости отелями отелями: от дешевых или от дорогих. Данные выводит в формате списка словарей с ключами:
      {id, name, streetAddress, label, distance, current}.
      При возникновении ошибки возвращает список с текстом ошибки"""
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": page_size, "checkIn": check_in,
                       "checkOut": check_out, "adults1": "1", "sortOrder": sort_order,
                       "locale": "ru_RU", "currency": "RUB"}
        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': api_key
            }
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        data = json.loads(response.text)
        # print(data)  # строка для отладки
        if data["result"] != "OK" or len(data['data']['body']['searchResults']['results']) == 0:
            raise LookupError
        hotels = []
        for i_hotel in data['data']['body']['searchResults']['results']:
            hotels.append(data_reader(i_hotel))
    except LookupError:
        hotels = ['Отелей не найдено']
    except ReadTimeout:
        hotels = ['Ошибка соединения']
    except ConnectionError:
        hotels = ['Ошибка соединения']
    except Exception as ex:
        hotels = [f'Ошибка: {ex}']
    return hotels
