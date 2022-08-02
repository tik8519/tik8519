# сравнение функций определения четности числа
import time

# + простота реализации и понимания
# + работает не только с целочисленными значениями
# - более медленная работа
def isEvent(value):
    return value % 2 == 0


# + более быстрая работа
# - не самая очевидная реализация
# - работа только с целочисленными значениями
def my_event(value):
    return not value & 1


if __name__ == '__main__':
    # сравнение времени выполнения алгоритмов
    x = 76567568685856

    start = time.time()
    for _ in range(1000000):
        isEvent(x)
    print(isEvent(x))
    print('Время выполнения:', round(time.time() - start, 2), 's')

    start = time.time()
    for _ in range(1000000):
        my_event(x)
    print(my_event(x))
    print('Время выполнения:', round(time.time() - start, 2), 's')
