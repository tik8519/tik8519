import time


def simple(number: int) -> list:
    """Функция генерирования списка простых чисел"""
    simple_number_list = [2]
    for num in range(3, number + 1, 2):
        for simple_number in simple_number_list:
            if num % simple_number == 0:
                break
            elif num ** 0.5 < simple_number:
                simple_number_list.append(num)
                break
    return simple_number_list


if __name__ == '__main__':
    # Определение времени генерации списка простых чисел, генерируемого циклом и условным оператором
    start: float = time.time()
    for _ in range(2000):
        simple(2000)
    print(simple(2000))
    print('Время выполнения:', round(time.time() - start, 2), 's')

    # Определение времени генерации списка простых чисел, генерируемого list comprehension
    start: float = time.time()
    for _ in range(2000):
        [2] + (list(filter(lambda x: all(map(lambda i: x % i != 0,
                                             range(3, int(x ** 0.5) + 1, 2))), range(3, 2000 + 1, 2))))
    print([2] + (list(filter(lambda x: all(map(lambda i: x % i != 0,
                                               range(3, int(x ** 0.5) + 1, 2))), range(3, 2000 + 1, 2)))))
    print('Время выполнения:', round(time.time() - start, 2), 's')
