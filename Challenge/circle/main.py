import math


class Circle:
    """Класс определяющий поведение окружности. Окружность имеет 2 координаты и радиус.
     Окружность может увеличиваться в размере, определяет свой периметр и площадь.
     Определяет, пересекается ли она с другими окружностями"""

    other_circles = []

    def __init__(self, X=0, Y=0, rad=1):
        """Инициализация экземпляра"""
        self.X = X
        self.Y = Y
        self.rad = rad
        self.index = len(Circle.other_circles)
        Circle.other_circles.append([X, Y, rad])
        print(f'Привет, Я новая окружность №{self.index + 1}. Мои координаты: ({X}, {Y}), мой радиус {rad}')

    def height(self, ratio):
        """Увеличивает диаметр окружности в ratio раз"""
        self.rad *= ratio
        Circle.other_circles[self.index][2] = self.rad
        print(f'Окр №{self.index + 1}: Теперь я выросла. Мой радиус {self.rad}')

    def square(self):
        """Определяет площадь окружности"""
        print(f'Окр №{self.index + 1}: Моя площадь: {round(math.pi * self.rad ** 2, 2)}')
        return round(math.pi * self.rad ** 2, 2)

    def perimeter(self):
        """Определяет периметр окружности"""
        print(f'Окр №{self.index + 1}: Мой периметр: {round(2 * math.pi * self.rad, 2)}')
        return round(2 * math.pi * self.rad, 2)

    def intersection(self):
        """Определяет, пересекается ли данная окружность с другими окружностями"""
        count = 0
        for circle in Circle.other_circles:
            min_rad = min(circle[2], self.rad)
            max_rad = max(circle[2], self.rad)
            sym_rad = circle[2] + self.rad
            distance_centers = math.sqrt((circle[0] - self.X) ** 2 + (circle[1] - self.Y) ** 2)
            if max_rad <= distance_centers < sym_rad:
                count += 1
            elif distance_centers < max_rad <= distance_centers + min_rad:
                count += 1
        if count > 1:
            print(f'Окр №{self.index + 1}: Кажется я с кем-то пересекаюсь')
        else:
            print(f'Окр №{self.index + 1}: Я ни с кем не пересекаюсь')


if __name__ == '__main__':
    # можно прописать логику действия окружностей или придумать сценарий их жизни
    circle1 = Circle()
    circle2 = Circle(2, 0, 2)
    circle1.square()
    circle2.perimeter()
    circle2.intersection()
    circle1.height(6)
    circle2.intersection()
