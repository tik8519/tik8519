from itertools import product
import copy


def converting_list(text):
    """Конвертирует введенное выражение в двумерный список, где каждый элемент вложенных списков это цифра
     составляющее число слагаемых и суммы соответственно."""
    text_list = list(text)  # преобразует введенный текст в список
    two_dimensional_list = [[], [], []]
    item = 0
    while text_list[item] != "+":
        two_dimensional_list[0].append(text_list[item])
        item += 1
    item += 1
    while text_list[item] != "=":
        two_dimensional_list[1].append(text_list[item])
        item += 1
    item += 1
    while len(text_list) > item:
        two_dimensional_list[2].append(text_list[item])
        item += 1
    return two_dimensional_list


def check(check_list):
    """Проверяет правильность суммы в 2-х мерном списке и печатает правильные выражения"""
    expression_list = [[], [], []]
    for i in range(3):
        number = 0
        for item in range(len(check_list[i])):
            number = number + int(check_list[i][item]) * 10 ** (len(check_list[i]) - 1 - item)
        expression_list[i] = number  # преобразует вложенные вписки в десятичные числа
    if expression_list[0] + expression_list[1] == expression_list[2]:
        print(f'{expression_list[0]}+{expression_list[1]}={expression_list[2]}')
        return True
    else:
        return False


def question_count(text):
    """Считает количество вопросов в выражении"""
    count = 0
    for symbol in text:
        if symbol == '?':
            count += 1
    return count


def checking_options(text):
    """Подставляет в список вместо "?" сгенерированные варианты. Если вариантов нет печатает: "impossible" """
    new_expression = converting_list(text)
    digit_list = [i for i in range(10)]
    generator = list(product(digit_list, repeat=question_count(text)))
    # Генерирует варианты комбинаций цифр на места знаков вопросов

    options_count = 0  # счетчик совпадений положительно прошедших проверку
    for item_option in range(len(generator)):  # вместо знаков вопроса подставляет сгенерированные цифры
        list_to_check = copy.deepcopy(new_expression)  # глубокая копия списка для проверки
        z = 0  # номер цифры из сгенерированного списка, которая следующая заменит знак вопроса в выражении
        for i in range(3):
            for t in range(len(list_to_check[i])):
                if list_to_check[i][t] == "?":
                    list_to_check[i][t] = str(generator[item_option][z])
                    z += 1

        if check(list_to_check):
            options_count += 1

    if options_count == 0:
        print("impossible")
    else:
        print(f'Нашлось вариантов: {options_count}')


# 45?+?5?=700 пример вводимых данных
if __name__ == '__main__':
    # по умолчанию считается, что данные вводятся корректно, поэтому нет проверок входящего выражения
    expression = input("Введите сумму:")
    checking_options(expression)
