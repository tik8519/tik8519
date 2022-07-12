import copy
from itertools import product


def converting_list(text):
    """Преобразует введенный текст в список в котором:
    '?' - 0
    '(' - 1
    ')' - -1"""
    text_list = list(text)
    converted_list = []  # список в который скобки и вопросы преобразуются в числа
    for item in text_list:
        if item == '?':
            converted_list.append(0)
        elif item == '(':
            converted_list.append(1)
        elif item == ')':
            converted_list.append(-1)
    return converted_list


def check(list_check):
    """Проверяет, является ли скобочное выражение правильным"""
    if sum(list_check) == 0:
        flag = None
        for i in range(len(list_check)):  # проверяет, что в любом месте списка есть только открытые скобки (сумма >= 0)
            current_amount = sum(list_check[0:i+1])
            if current_amount >= 0:
                flag = True
            else:
                flag = False
                break
        return flag
    else:
        return False


def question_counter(list_check):
    """Считает количество '0' в выражении"""
    question_count = 0
    for item in list_check:
        if item == 0:
            question_count += 1
    return question_count


def selection_solution(list_check):
    """Генерирует варианты замены знаков ? и считает количество правильных вариантов"""
    variants = [-1, 1]
    generator = product(variants, repeat=question_counter(list_check))
    # генерирует сочетания значений из списка variants в количестве знаков '?' выражения
    counter_good_variants = 0
    for item_variants in generator:
        new_list_check = copy.deepcopy(list_check)
        count_item = 0  # указывает номер сгенерированного символа подставляемого вместо "?"
        for i in range(len(new_list_check)):
            if new_list_check[i] == 0:
                new_list_check[i] = item_variants[count_item]
                count_item += 1
        if check(new_list_check):
            print(new_list_check)
            counter_good_variants += 1
    return counter_good_variants


# Скопировать: ????(?
if __name__ == '__main__':
    combination = input("Введите комбинацию: ")
    print(f'Количество вариантов: {selection_solution(converting_list(combination))}')
