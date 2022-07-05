def print_arena(filling):
    """Выводит не печать игровое поле"""
    print(f'\n  {filling[0]}  |  {filling[1]}  |  {filling[2]}\n'
          f'-----|-----|-----\n'
          f'  {filling[3]}  |  {filling[4]}  |  {filling[5]}\n'
          f'-----|-----|-----\n'
          f'  {filling[6]}  |  {filling[7]}  |  {filling[8]}')


def check(filling):
    """Проверяет не победил ли кто то"""
    winner = False
    for i in range(0, 7, 3):
        if filling[i] == filling[i + 1] == filling[i + 2]:
            winner = True
    for i in range(3):
        if filling[i] == filling[i + 3] == filling[i + 6]:
            winner = True
    if filling[0] == filling[4] == filling[8]:
        winner = True
    elif filling[2] == filling[4] == filling[6]:
        winner = True
    return winner


def motion(symbol, filling):
    """Предлагает ввести номер ячейки для хода и проверяет корректность ввода данных"""
    while True:
        try:
            choice = int(input(f'В какую ячейку поставить {symbol}? '))
            if choice == filling[choice - 1]:
                filling[choice - 1] = symbol
                break
            else:
                raise ValueError
        except ValueError and IndexError:
            print('Ошибка ввода. Попробуйте еще.')


def game():
    """Игровая логика"""
    filling = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    count = 0
    while True:
        if count % 2 == 0:
            unit = 'X'
        elif count % 2 == 1:
            unit = 'O'
        print_arena(filling)
        motion(unit, filling)
        if check(filling):
            print_arena(filling)
            print(f'Поздравляем, победил {unit}!')
            break
        count += 1


if __name__ == '__main__':
    game()
