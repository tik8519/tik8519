import ast
import datetime
import os


def load_history(user_dict: dict) -> None:
    """Сохраняет в файл: 'history.log' всю информацию которая сохранялась в словаре пользователя"""
    if os.path.getsize(os.path.join('logs', 'history.log')) > 500000:
        with open(os.path.join('logs', 'history.log'), 'w', encoding='utf-8') as file:
            file.write('')
    data = f'{user_dict}\n'
    with open(os.path.join('logs', 'history.log'), 'a', encoding='utf-8') as file:
        file.write(data)


def read_history(user_id: int) -> list:
    """По id пользователя берет из файла history.log информацию о том, что искал пользователь и
     возвращает в виде списка.
     Информацию выводит о запросах не позднее 7-ми дней от текущей даты и не более 20-ти запросов."""
    user_history = []
    with open(os.path.join('logs', 'history.log'), 'r', encoding='utf-8', ) as file:
        for i_request in file:
            history_request = ast.literal_eval(str(i_request))
            date = datetime.datetime.strptime(history_request['time'], '%Y-%m-%d %H:%M:%S')
            if history_request['user_id'] == user_id and datetime.datetime.today() - date < datetime.timedelta(days=7):
                if len(user_history) >= 20:
                    user_history.pop(0)
                user_history.append(history_request)
    return user_history
