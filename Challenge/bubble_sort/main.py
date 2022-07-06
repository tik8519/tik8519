def sort_list(order):
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


if __name__ == '__main__':
    roster = [1, 4, -3, 0, 10, 4, 6]
    print(f'Изначальный список: {roster}')
    print(f'Сортированный список: {sort_list(roster)}')
