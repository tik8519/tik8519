import os
import zipfile


def analysis_text(zip_name, file_name):
    with zipfile.ZipFile(zip_name, 'r') as zip_file:
        zip_file.extract(file_name, '.')

    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    with open(file_name, 'r', encoding='utf-8') as speakers_file:
        symbol_dict = {}
        garbage = {}

        for i_line in speakers_file:
            for symbol in i_line:
                if symbol in letters:
                    if symbol in symbol_dict.keys():
                        symbol_dict[symbol] += 1
                    else:
                        symbol_dict[symbol] = 1
                else:
                    if symbol in garbage.keys():
                        garbage[symbol] += 1
                    else:
                        garbage[symbol] = 1

    os.remove(file_name)

    with open('analysis.txt', 'w', encoding='utf-8') as resul:
        for score in reversed(sorted(symbol_dict.values())):
            for key in symbol_dict.keys():
                if symbol_dict[key] == score:
                    resul.write(f'{key} {score}\n')
                    symbol_dict[key] = 0
        resul.write(f'Прочие символы: {garbage}\n')


if __name__ == '__main__':
    file = 'voyna-i-mir.txt'
    archive = 'voyna-i-mir.zip'
    analysis_text(archive, file)
