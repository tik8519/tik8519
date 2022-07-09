import os
import telebot
import datetime
from functions.history import load_history, read_history
from functions.city_id import city_id
from functions.lowprice import lowprice
from functions.bestdeal import bestdeal
from functions.show_foto import roster_foto
from loguru import logger


TOKEN = os.getenv("DIPLOMHOTELBOTTOKEN")
KEY: str = os.getenv("RAPIDAPIKEY")
bot = telebot.TeleBot(TOKEN)

logger.add(os.path.join('logs', 'error.log'), rotation='5 MB', compression='zip')


@bot.message_handler(content_types=['text'])
def start(message) -> None:
    """Выводит приветственное сообщение."""
    user = dict()
    try:
        bot.send_message(message.from_user.id, 'Приветствую вас, я помогу найти подходящий вам отель.\n'
                                               'Можете указать одну из команд:\n'
                                               '/help - я расскажу, что умею,\n'
                                               '/history - вывод истории поиска отелей.\n'
                                               'Или УКАЖИТЕ ГОРОД для поиска отелей.')
        user['user_id']: int = message.from_user.id
        bot.register_next_step_handler(message, get_city, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def get_city(message, user: dict) -> None:
    """Определяет что ввел пользователь. Если команду '/help' или '/history', то вызывает соответствующую команду.
     Если введена не команда, то вызывает функцию city_id."""
    try:
        if '/' in message.text:
            if message.text == '/help':
                bot_help(message, user)
            elif message.text == '/history':
                history(message, user)
            else:
                bot.send_message(message.from_user.id, 'Я не знаю такую команду.\n'
                                                       'Введите что нибудь что бы попробовать ещё раз.')
        else:
            user_city: [int, str] = city_id(message.text, KEY)
            if isinstance(user_city, int):
                bot.send_message(message.from_user.id, 'Я знаю такой город!')
                user['city'] = message.text
                user['city_id'] = user_city
                bot.send_message(message.from_user.id, 'Теперь введите одну из команд:\n'
                                                       '/lowprice - вывод самых дешёвых отелей в городе,\n'
                                                       '/highprice - вывод самых дорогих отелей в городе,\n'
                                                       '/bestdeal - вывод отелей, наиболее подходящих'
                                                       ' по цене и расположению от центра.')
                bot.register_next_step_handler(message, command, user)
            else:
                bot.send_message(message.from_user.id, 'Я не нашел такой город.\nВведите город еще раз.')
                bot.register_next_step_handler(message, get_city, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def bot_help(message, user: dict) -> None:
    """Выводит сообщение с текстом помощи."""
    try:
        bot.send_message(user['user_id'], 'Основные шаги для поиска:\n'
                                          '1) Укажите город поиска.\n'
                                          '2) Выберите команду, которая определяет принцип поиска отеля.\n'
                                          '3) Отвечая на запросы, введите уточняющую информацию.\n'
                                          '4) Получив результат поиска, можно посмотреть фотографии отелей.\n')
        start(message)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def history(message, user: dict) -> None:
    """Вызывает функцию read_history. Если история найдена, выводится краткая информация по каждому запросу."""
    my_history: list = read_history(user['user_id'])
    if len(my_history) == 0:
        bot.send_message(user['user_id'], 'История не найдена.\nВведите что нибудь что бы продолжить.')
    else:
        bot.send_message(user['user_id'], f'Найдено запросов: {len(my_history)}')
        counter = 1
        for i_request in my_history:
            bot.send_message(user['user_id'], f"Запрос № {counter}\n"
                                              f"Время запроса: {i_request['time']}\n"
                                              f"Город: {i_request['city']}\n"
                                              f"Команда для поиска: {i_request['command']}")
            counter += 1
        bot.send_message(user['user_id'], 'Укажите номер запроса что бы увидеть подробности.\n'
                                          'Укажите 0 что бы начать заново.')
    bot.register_next_step_handler(message, history_details, user, my_history)


def history_details(message, user: dict, my_history: list) -> None:
    """Выводит более подробную информацию по выбранному пользователем запросу."""
    try:
        if 0 < int(message.text) <= len(my_history):
            number = int(message.text) - 1
            bot.send_message(message.from_user.id, f"Запрос № {int(message.text)}\n"
                                                   f"Время запроса: {my_history[number]['time']}\n"
                                                   f"Город: {my_history[number]['city']}\n"
                                                   f"Команда для поиска: {my_history[number]['command']}\n"
                                                   f"Даты проживания: {my_history[number]['check_in']} - "
                                                   f"{my_history[number]['check_out']}\n"
                                                   f"Были найдены следующие отели:")
            counter = 1
            for i_hotel in my_history[number]['hotels']:
                bot.send_message(message.from_user.id, f"Запрос № {counter}\n"
                                                       f"Отель: {i_hotel['name']}\n"
                                                       f"Цена проживания: {i_hotel['exactCurrent']} RUB")
                bot.send_message(message.chat.id, f"[{i_hotel['name']}](https://ru.hotels.com/ho{i_hotel['id']}/"
                                                  f"?q-check-in={my_history[number]['check_in']}"
                                                  f"&q-check-out={my_history[number]['check_out']}"
                                                  f"&q-rooms=1&q-room-0-adults=1", parse_mode='Markdown')
                counter += 1
        elif int(message.text) == 0:
            start(message)
        else:
            raise ValueError
    except ValueError:
        bot.send_message(message.from_user.id, 'Не корректно введен номер запроса.\nПопробуйте ещё раз.')
        bot.register_next_step_handler(message, history_details, user, my_history)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def command(message, user: dict) -> None:
    """Определяет какую команду с типом поиска ввел пользователь. В зависимости от выбора вызываются функции
     с необходимыми запросами."""
    try:
        if message.text in ('/lowprice', '/highprice'):
            bot.send_message(message.from_user.id, 'Сколько отелей отображать в поиске?\n'
                                                   'Максимум 25.')
            user['command'] = message.text
            bot.register_next_step_handler(message, check_in, user)
        elif message.text == '/bestdeal':
            user['command'] = message.text
            bot.send_message(message.from_user.id, 'Введите минимальную цену проживания за сутки в рублях.')
            bot.register_next_step_handler(message, min_cost, user)
        else:
            bot.send_message(message.from_user.id, 'Я не знаю такую команду.\n'
                                                   'Введите одну из следующих команд:'
                                                   ' /lowprice, /highprice, /bestdeal.')
            bot.register_next_step_handler(message, command, user)
        user['time'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def min_cost(message, user: dict) -> None:
    """Вызывается если пользователь ввел команду: '/bestdeal'. Проверяет корректный ввод минимальной цены для поиска."""
    try:
        if int(message.text) < 0:
            raise ValueError
        user['min_cost'] = int(message.text)
        bot.send_message(message.from_user.id, 'Введите максимальную цену проживания за сутки')
        bot.register_next_step_handler(message, max_cost, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Цена за сутки проживания должна быть положительным числом.\n'
                                               'Введите цену еще раз.')
        bot.register_next_step_handler(message, min_cost, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def max_cost(message, user: dict) -> None:
    """Вызывается если пользователь ввел команду: '/bestdeal'.
    Проверяет корректный ввод максимальной цены для поиска."""
    try:
        if int(message.text) <= user['min_cost']:
            raise ValueError
        user['max_cost'] = int(message.text)
        bot.send_message(message.from_user.id, 'Введите минимальное расстояние от центра города до отеля в километрах')
        bot.register_next_step_handler(message, min_distance, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Максимальная цена за сутки проживания должна быть больше минимальной.\n'
                                               'Введите цену еще раз.')
        bot.register_next_step_handler(message, max_cost, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def min_distance(message, user: dict) -> None:
    """Вызывается если пользователь ввел команду: '/bestdeal'. Проверяет корректный ввод минимальной дистанции от центра
     для поиска отелей."""
    try:
        if int(message.text) < 0:
            raise ValueError
        user['min_distance'] = int(message.text)
        bot.send_message(message.from_user.id, 'Введите максимальное расстояние от центра города до отеля в километрах')
        bot.register_next_step_handler(message, max_distance, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое положительное число.\nПопробуйте ещё раз.')
        bot.register_next_step_handler(message, min_distance, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def max_distance(message, user: dict) -> None:
    """Вызывается если пользователь ввел команду: '/bestdeal'. Проверяет корректный ввод максимальной дистанции
     от центра для поиска отелей."""
    try:
        if int(message.text) < user['min_distance']:
            raise ValueError
        user['max_distance'] = int(message.text)
        bot.send_message(message.from_user.id, 'Сколько отелей отображать в поиске?\n'
                                               'Максимум 25.')
        bot.register_next_step_handler(message, check_in, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Максимальная дистанция от центра города должна быть больше'
                                               ' минимальной.\nВведите максимальную дистанцию еще раз.')
        bot.register_next_step_handler(message, max_distance, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def check_in(message, user: dict) -> None:
    """Проверяет корректность ввода количества отелей для отображения. Запрашивает дату заселения."""
    try:
        if 0 < int(message.text) < 25:
            page_size = int(message.text)
        elif int(message.text) == 0:
            raise SyntaxError
        else:
            page_size = 25
        user['page_size'] = page_size
        bot.send_message(message.from_user.id, 'Укажите дату заселения в формате День-Месяц-Год\n'
                                               'Например: 10-02-2022')
        bot.register_next_step_handler(message, check_out, user)
    except SyntaxError:
        bot.send_message(message.from_user.id, 'Странный ответ.\nУкажите город еще раз.')
        bot.register_next_step_handler(message, get_city, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Необходимо ввести число.')
        bot.register_next_step_handler(message, check_in, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def check_out(message, user: dict) -> None:
    """Проверяет корректность ввода даты заселения. Запрашивает количество ночей прибывания в отеле."""
    try:
        date = datetime.datetime.strptime(message.text, '%d-%m-%Y')
        date_today = datetime.datetime.today() - datetime.timedelta(days=1)
        if date < date_today:
            bot.send_message(message.from_user.id, 'Этот день уже прошёл.')
            raise ValueError
        user['check_in'] = datetime.datetime.strftime(date, '%Y-%m-%d')
        bot.send_message(message.from_user.id, 'Укажите сколько ночей вы планируете провести в отеле.')
        bot.register_next_step_handler(message, choice, user)
    except ValueError:
        bot.send_message(message.from_user.id, 'Дата введена некорректно.\n'
                                               'Попробуйте ещё раз.')
        bot.register_next_step_handler(message, check_out, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def choice(message, user: dict) -> None:
    """Проверяет корректность ввода количество ночей прибывания в отеле.
     Вызывает функцию соответствующую команде поиска указанной пользователем.
     Отображает результаты поиска."""
    try:
        bot.send_message(message.from_user.id, f'Ищу отели.\nЭто займет не больше минуты.')
        days = int(message.text)
        if days <= 0:
            days = 1
        user['days'] = days
        date_check_out = datetime.datetime.strptime(user['check_in'], '%Y-%m-%d') + datetime.timedelta(days=days)
        user['check_out'] = datetime.datetime.strftime(date_check_out, '%Y-%m-%d')
        if user['command'] == '/lowprice':
            sort_order = 'PRICE'
            hotel_list = lowprice(user['city_id'], KEY, user['check_in'], user['check_out'], sort_order,
                                  page_size=user['page_size'])
        elif user['command'] == '/highprice':
            sort_order = 'PRICE_HIGHEST_FIRST'
            hotel_list = lowprice(user['city_id'], KEY, user['check_in'], user['check_out'], sort_order,
                                  page_size=user['page_size'])
        elif user['command'] == '/bestdeal':
            query_string = {
                "destinationId": user['city_id'], "pageNumber": 1, "pageSize": '25',
                "checkIn": user['check_in'], "checkOut": user['check_out'], "adults1": "1",
                "priceMin": user['min_cost'], "priceMax": user['max_cost'], "sortOrder": "DISTANCE_FROM_LANDMARK",
                "locale": "ru_RU", "currency": "RUB"
            }
            hotel_list = bestdeal(query_string, KEY, user['min_distance'], user['max_distance'], user['page_size'])
        else:
            hotel_list = ['Это не вероятно!']
        # print(hotel_list)  # строка для отладки
        if not isinstance(hotel_list[0], str):
            counter = 1
            user['hotels'] = []
            for i_hotel in hotel_list:
                bot.send_message(message.from_user.id, f"Отель №{counter}:\n{i_hotel['name']}\n"
                                                       f"Адрес: {i_hotel['streetAddress']}\n"
                                                       f"{i_hotel['label']}: {i_hotel['distance']}\n"
                                                       f"Цена: {int(i_hotel['exactCurrent'])} RUB {i_hotel['info']}")
                bot.send_message(message.chat.id, f"[{i_hotel['name']}](https://ru.hotels.com/ho{i_hotel['id']}/"
                                                  f"?q-check-in={user['check_in']}&q-check-out={user['check_out']}"
                                                  f"&q-rooms=1&q-room-0-adults=1", parse_mode='Markdown')
                user['hotels'].append(i_hotel)  # переписать что бы сохранялась вся инфа об отелях
                if counter == user['page_size']:
                    break
                counter += 1
            bot.send_message(message.from_user.id, 'Укажите номер отеля для просмотра фото.\n'
                                                   'Укажите 0, если показывать фото не нужно.')
            bot.register_next_step_handler(message, show_foto, user)
        else:
            load_history(user)
            bot.send_message(message.from_user.id, f'{hotel_list[0]}. Напишите что нибудь что бы попробовать ещё раз.')
    except ValueError:
        bot.send_message(message.from_user.id, 'Необходимо ввести число.')
        bot.register_next_step_handler(message, choice, user)
    except Exception as ex:
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


def show_foto(message, user: dict) -> None:
    """Проверяет корректность ввода пользователем номера отеля для показа фото.
     Показывает 5 фотографий выбранного отеля."""
    try:
        number = int(message.text)
        if 0 < number <= len(user['hotels']):
            hotel_id = user['hotels'][number - 1]['id']
            bot.send_message(message.from_user.id, "Сейчас покажу фото. Это займет не больше минуты.")
            url_list = roster_foto(hotel_id, KEY, count=5)
            if isinstance(url_list, str):
                bot.send_message(message.from_user.id, f'{url_list}\nВведите что нибудь что бы продолжить.')
            else:
                bot.send_message(message.from_user.id, f"Фото отеля: {user['hotels'][number - 1]['name']}")
                user['foto'] = []
                for url in url_list:
                    bot.send_photo(message.chat.id, photo=url)
                    user['foto'].append(url)
                bot.send_message(message.from_user.id, 'Укажите номер отеля для просмотра фото.\n'
                                                       'Укажите 0, если показывать фото не нужно.')
                bot.register_next_step_handler(message, show_foto, user)
        elif number >= len(user['hotels']):
            bot.send_message(message.from_user.id, 'Отеля с таким номером нет.\n'
                                                   'Попробуйте ещё раз.')
            bot.register_next_step_handler(message, show_foto, user)
        else:
            bot.send_message(message.from_user.id, 'Надеюсь я был полезен.\nВведите что-нибудь что бы повторить.')
            load_history(user)
        # print(user) # строка для отладки
    except ValueError:
        load_history(user)
        bot.send_message(message.from_user.id, 'Необходимо ввести число.')
        bot.register_next_step_handler(message, show_foto, user)
    except Exception as ex:
        load_history(user)
        logger.error(f'Ошибка: {ex} | Последнее сообщение: {message.text} | Данные пользователя: {user}')
        bot.send_message(message.from_user.id, f'Произошла непредвиденная ошибка.\nПопробуйте ещё раз.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
