def seating():
    girls = int(input('Введите кол-во девочек: '))
    boys = int(input('Введите кол-во мальчиков: '))
    if boys == 0 or girls == 0:
        print('Ответ: Нет решения')
    elif boys / girls > 2 or girls / boys > 2:
        print('Ответ: Нет решения')
    else:
        if boys >= girls:
            majority = boys
            minority = girls
            triple_symbol = str('BGB')
            double_symbol = str('GB')
        else:
            majority = girls
            minority = boys
            triple_symbol = str('GBG')
            double_symbol = str('BG')
            difference = majority - minority
        print(f'Ответ: {triple_symbol * difference + double_symbol * (minority - difference)}')


if __name__ == '__main__':
    seating()
