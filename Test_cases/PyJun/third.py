# реализация функции сортировки
# выбор реализации алгоритма сортировки должен учитывать "запутанность" изначального массива
import copy


def sort_list(order):
    # пузырьковая сортировка, количество перестановок зависит от изначальной упорядоченности и может быть либо больше
    # кол-ва элементов, так и меньше
    swap = 0
    while True:
        counter = 0
        for i in range(len(order)-1):
            if order[i] > order[i+1]:
                order[i], order[i+1] = order[i+1], order[i]
                counter += 1
                swap += 1
        if counter == 0:
            break
    print(f'Количество перестановок: {swap}')
    return order


def max_sort_list(order):
    # сортировка по минимальному значению, количество перестановок всегда равно кол-ву элементов
    length = len(order)
    for i in range(length):
        max_item = min(order[:length-i])
        order.remove(max_item)
        order.append(max_item)
    return order


if __name__ == '__main__':
    roster = [1, 4, -3, 0, 10, 4, 6, -4]
    roster2 = copy.deepcopy(roster)
    print(f'Изначальный список: {roster}')
    print(f'1) Сортированный список: {sort_list(roster)}')
    print(f'2) Сортированный список: {max_sort_list(roster2)}')
