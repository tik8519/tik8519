import json
from requests import ReadTimeout
import requests


def roster_foto(hotel_id, api_key, count=5):
    try:
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": hotel_id}
        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': api_key
            }
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        data = json.loads(response.text)
        result = []
        url_count = 0
        for i_image in data["hotelImages"]:
            suffix = i_image["sizes"][0]["suffix"]
            foto_url = i_image["baseUrl"].replace("{size}", suffix)
            result.append(foto_url)
            url_count += 1
            if url_count == count:
                break
    except ReadTimeout:
        result = ['Ошибка соединения']
    except ConnectionError:
        result = ['Ошибка соединения']
    except Exception as ex:
        result = [f'Ошибка: {ex}']
    return result
