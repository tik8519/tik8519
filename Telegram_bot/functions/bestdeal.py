import json
import requests
from requests import ReadTimeout


def float_dist(text_dist: str) -> float:
    """Принимает значение расстояния в виде текста, отбрасывает 'км' и переводит в числовое значение."""
    dist = text_dist[:-3].split(',')
    if len(dist) == 1:
        digit_dist = int(dist[0])
    elif len(dist) == 2:
        digit_dist = int(dist[0]) + int(dist[1]) / 10
    else:
        digit_dist = None
    return digit_dist


def data_reader(hotel: dict) -> dict:
    api_keys = [hotel, hotel, hotel["address"], hotel["landmarks"][0], hotel["landmarks"][0],
                hotel["ratePlan"]["price"], hotel["ratePlan"]["price"], hotel["ratePlan"]["price"]]
    bot_keys = ['id', 'name', 'streetAddress', 'label', 'distance', 'current', 'exactCurrent', 'info', ]
    bot_hotel = dict()
    for i_api_keys, i_bot_keys in zip(api_keys, bot_keys):
        try:
            bot_hotel[i_bot_keys] = i_api_keys[i_bot_keys]
        except KeyError:
            bot_hotel[i_bot_keys] = 'нет данных'
    return bot_hotel


def bestdeal(querystring: dict, api_key: str, min_dist: int, max_dist: int, hotel_size: int) -> list:
    """Делает запрос на rapidapi.com по отелям с заданным диапазоном цен за ночь проживания и выберет отели
     по заданному диапазону расстояний от центра. Если количества найденных отелей не достаточно, делает повторный
      запрос на следующую страницу отелей. Если во время работы функции возникает ошибка, в списке передается
       информацию об ошибке. Данные выводит в формате списка словарей с ключами:
       {id, name, streetAddress, label, distance, current}"""
    try:
        my_data = list()
        search_flag = True
        while search_flag:
            url = "https://hotels4.p.rapidapi.com/properties/list"
            headers = {
                'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': api_key
                }
            response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
            data = json.loads(response.text)
            # print(data)  # строка для отладки
            if data["result"] != "OK" or len(data['data']['body']['searchResults']['results']) == 0:
                search_flag = False

            for i_hotel in data['data']['body']['searchResults']['results']:
                dist = float_dist(i_hotel["landmarks"][0]["distance"])
                if min_dist <= dist <= max_dist:
                    my_data.append(data_reader(i_hotel))
                elif dist > max_dist:
                    search_flag = False
            if len(my_data) >= hotel_size:
                search_flag = False
            querystring["pageNumber"] += 1

        if len(my_data) == 0:
            my_data = ['Отелей не найдено']
        hotels = my_data

    except LookupError:
        hotels = ['Отелей не найдено']
    except ReadTimeout:
        hotels = ['Ошибка соединения']
    except ConnectionError:
        hotels = ['Ошибка соединения']
    except Exception as ex:
        hotels = [f'Ошибка: {ex}']
    return hotels
