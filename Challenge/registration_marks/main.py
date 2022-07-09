import re


if __name__ == '__main__':
    text: str = 'А578ВЕ777 ОР233787 К901МН666 СТ46599 СНИ2929П777 666АМР666 А578ВЕ77'

    car_number: str = re.findall(r'\b[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}\b', text)
    print('Список номеров частных автомобилей:', car_number)

    taxi_number: str = re.findall(r'\b[АВЕКМНОРСТУХ]{2}\d{5,6}\b', text)
    print('Список номеров такси:', taxi_number)
