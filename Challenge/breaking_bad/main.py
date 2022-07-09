from typing import Dict, List
import requests
import json


def breaking_deaths_rating() -> Dict:
    """Функция нахождения эпизода из сериала “Во все тяжкие” с самым большим числом жертв
    Данные берутся с API https://breakingbadapi.com
    Результат выводит в формате словаря с ключами:
    Id эпизода
    Номер сезона
    Номер эпизода
    Общее количество смертей
    Список погибших"""

    episodes_info = requests.get('https://breakingbadapi.com/api/episodes')
    deaths_info = requests.get('https://breakingbadapi.com/api/deaths')

    data_episodes = json.loads(episodes_info.text)
    data_deaths = json.loads(deaths_info.text)

    breaking_list: List = list()

    for episodes in data_episodes:
        if episodes['episode_id'] > 62:
            break
        cash_dict: Dict = dict()
        cash_dict['episode_id'] = episodes['episode_id']
        cash_dict['season'] = int(episodes['season'])
        cash_dict['episode'] = int(episodes['episode'])
        cash_dict['all_deaths'] = 0
        cash_dict['list_deaths'] = []

        for deaths in data_deaths:
            if deaths['season'] == int(episodes['season']) and deaths['episode'] == int(episodes['episode']):
                cash_dict['all_deaths'] += deaths['number_of_deaths']
                cash_dict['list_deaths'].append(deaths['death'])

        breaking_list.append(cash_dict)

    max_deaths_episode: Dict = dict()
    max_deaths: int = 0
    for episodes in breaking_list:
        if episodes['all_deaths'] > max_deaths:
            max_deaths = episodes['all_deaths']
            max_deaths_episode = episodes

    return max_deaths_episode


if __name__ == '__main__':
    result: Dict = breaking_deaths_rating()

    with open('result.json', 'w') as file:
        json.dump(result, file, indent=4)

    print(f"В эпизоде {result['episode']} сезона {result['season']}"
          f" умерло: {result['all_deaths']} - это эпизод с самым большим количеством смертей")
