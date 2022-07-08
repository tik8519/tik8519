import random


class Players:
    """Класс игрока. Хранит данные о руке игрока. Сдает карты из колоды. Считает счет руки."""
    card_list = [x * 100 + i for x in range(1, 5) for i in range(2, 15)]
    # Генерирует колоду карт трехзначными числами. Сотни - масти, десятки - номинал.

    def __init__(self):
        self.hand = []
        self.score = 0

    def give_card(self):
        """Раздает карты"""
        i = random.randint(0, len(Players.card_list) - 1)  # определяет случайный номер карты из колоды
        self.hand.append(Players.card_list.pop(i))  # Передает карту игроку и удаляет её из списка колоды

    def count_points(self):
        """Считает очки игрока"""
        self.score = 0
        score_hand = []  # Список со значениями номинала карт
        for card in self.hand:
            score_hand.append(int(card % 100))
        score_hand.sort()  # Сортировка нужна для правильного определения значения туза

        for card in score_hand:
            if 2 <= card < 10:
                self.score += card
            elif 10 <= card <= 13:
                self.score += 10
            elif card == 14 and self.score < 21:
                self.score += 11
            elif card == 14 and self.score >= 21:
                self.score += 1
        return self.score

    def print_hand(self):
        """Выводит значение руки игрока в понятном человеку виде"""
        card_color = {1: 'пик', 2: 'червей', 3: 'бубей', 4: 'треф'}
        card_nominal = {2: 'двойка',
                        3: 'тройка',
                        4: 'четверка',
                        5: 'пятерка',
                        6: 'шестерка',
                        7: 'семерка',
                        8: 'восмерка',
                        9: 'девятка',
                        10: 'десятка',
                        11: 'валет',
                        12: 'дама',
                        13: 'король',
                        14: 'туз'}
        you_card = ''
        for card in self.hand:
            you_card += f'{card_nominal[int(card % 100)]} {card_color[int(card // 100)]}, '
        return you_card


def game_logic():
    """Определяет логику игры"""
    player = Players()
    croupier = Players()

    for _ in range(2):
        player.give_card()
        croupier.give_card()

    print('Ваши карты: ', player.print_hand())
    print('Ваш счет: ', player.count_points())

    answer = input('Берем еще карту?(да/нет): ')
    if answer == 'да':
        player.give_card()
        print('Ваши карты: ', player.print_hand())
        print('Ваш счет: ', player.count_points())

    croupier.count_points()
    if player.score > 21:
        print('Перебор! Победил крупье')
    elif player.score > croupier.score:
        print('Вы победили!')
    elif player.score < croupier.score:
        print('Победил крупье!')
    elif player.score == croupier.score:
        print('Ничья!')
    print('\nКарты крупье:', croupier.print_hand())
    print('Счет крупье:', croupier.score)


if __name__ == '__main__':
    game_logic()
