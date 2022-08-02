﻿## Алгоритм анализа данных
- определение наиболее коррелирующих данных с каждым из столбцом «target», при этом отсеяв строки в которых есть nan-элементы
- обучение нейросетей на основании выявленных столбцов
- заполнение nan-элементов в исходных данных для анализа средними значениями всего столбца
- получение прогнозных данных с помощью обученных нейросетей

###Полученная точность: 
- target1: 335%, 
- target2: 15%, 
- target3: 1%, 
- target4: 18%

###Наиболее значимые столбцы данных:
- tag59 корреляция: 0.87 c target4
- tag1 корреляция: около 0.3 с target1..3
- tag15 корреляция: около 0.3 с target1..3
- tag19 корреляция: около 0.3 с target1..3
- tag33 корреляция: около 0.3 с target1..3
- tag49 корреляция: около 0.5 с target1..3
- tag67 корреляция: около 0.5 с target1..3
- tag71 корреляция: около 0.3 с target1..3
- tag75 корреляция: около 0.5 с target1..3
- tag76 корреляция: около 0.3 с target1..3

#### для анализа использовались дополнительные библиотеки Numpy, Keras, Sqlite3



