import os, csv
import re
import pickle
import numpy as np


# процедура генерация таблиц языков из txt-файлов в директории data
def lang_generate_csv():
    reg = re.compile("\d+")  # регулярное выражение для захвата числа в строке
    for file in os.listdir('data'):  # смотрим доступнные данные
        if file.endswith(".txt"):  # указываем, что нужно расширение .txt
            file_name = file.split('.')[0]  # название файла
            # print(file_name.split('_')[0]) # выводим название языка (то что до знака '_')
            with open("languages/" + file_name + ".csv", 'w') as file_csv:
                with open("data/" + file_name + ".txt", 'r') as file:
                    lines = file.readlines()  # берем строки из файла

                    count = 0  # здесь будет сумма абсолютных частот
                    for line in lines:
                        number = (int)(re.findall(reg, line)[0])  # берем число из строки файла и преобразуем в int
                        count += number  # считаем абсолютную частоту всех символов

                    csv_writer = csv.writer(file_csv)  # готовимся записывать в таблицу
                    data = []  # пустой список для записи в строку csv-файла
                    checksum = 0  # для проверки суммы относительных частот
                    for line in lines:
                        ch = line.split()[0].lower()  # берем символ из строки txt-файла
                        number = (int)(re.findall(reg, line)[0])  # берем число из строки txt-файла
                        fr = number / count  # считаем относительную частоту
                        checksum += fr  # суммируем частоты (должно получиться число от 1-eps до 1+eps)
                        # добавляем элементы к нашему пустому списку
                        data.append(ch)
                        data.append(fr)
                        csv_writer.writerow(data)  # записываем
                        # print(data) # выводим, что записываем в строку таблицы
                        data.clear()  # чистим список
                    # print("checksum =",checksum)
    return None


# процедура генерации словаря языков
def lang_generate_langrec():
    langrec = {}
    langrec['languages'] = []
    langrec['characters'] = {}
    for file_name in os.listdir('languages'):  # переходим в готовые таблицы наших языков
        if file_name.endswith('.csv'):  # если это таблица, то...
            lang_name = file_name.split('_')[0]
            with open('languages/' + file_name, 'r') as file_csv:
                if lang_name not in langrec['languages']:  # если нет языка в списке языков, то...
                    langrec['languages'].append(lang_name)  # ...заносим в список
                langrec[lang_name + '_dict'] = {}  # здесь будет словарь языка
                langrec[lang_name + '_vector'] = []

                rows = csv.reader(file_csv)  # берем ряды таблицы
                for row in rows:
                    ch = row[0]  # берем символ
                    fr = float(row[1])
                    if ch not in langrec['characters']:  # если символа нет
                        langrec['characters'][ch] = 1  # заносим его, встретили первый раз
                    else:
                        langrec['characters'][ch] += 1  # иначе увидели еще одно вхождение в алфавит другого языка

                    langrec[lang_name + '_dict'][ch] = fr  # заносим букву в словарь языка

                # print(lang_name + " is listed") # выводим, что закончили с языком
                # print(' updated number of characters =', len(langrec['characters'])) # посмотрим на колво символов
    # теперь, когда мы знаем все возможные буквы, мы можем делать векторы языков
    # размерность таких векторов должна быть равна размерности колву всевозможных букв
    # для упорядоченности, будем идти по ключам characters и строить вектор каждого языка
    for lang_name in langrec['languages']:  # выбираем язык
        for ch in langrec['characters']:  # берем очередную букву из всех возможных
            if ch in langrec[lang_name + '_dict']:  # если такая буква есть в словаре языка
                langrec[lang_name + '_vector'].append(langrec[lang_name + '_dict'][ch])  # добавляем частоту буквы
            else:
                langrec[lang_name + '_vector'].append(0.0)  # иначе на этой позиции частота 0
    '''
    # выводим полученную структуру
    print('\n\n====LANGREC (dict)====')
    for key in langrec:
        print(key+':\n  ',langrec[key])
    print('======================\n')
    # проверим, не нарушили ли мы размерность
    for lang_name in langrec['languages']:
        print('size of '+lang_name+'_vector', len(langrec[lang_name+'_vector']))
    '''
    # сохраним словарь (чтобы заново его не делать, на основе этих языков)
    name = 'langrec_monograms'
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(langrec, f, pickle.HIGHEST_PROTOCOL)
    return None


# процедура генерация файлов и словаря (чтобы добавили языки, нажали кнопку и полетели)
def lang_generate():
    lang_generate_csv()
    lang_generate_langrec()
    return None


# функция превращения текста в вектор (размерность из словаря языков)
def text_to_vec(text):
    delim = """ .?!:,;-_―"'’‘“”„§€$£%&—/\⁄()[]{}+*~#´`^°•…=<>«»–|0123456789"""
    name = 'langrec_monograms'  # имя словаря языков
    with open('obj/' + name + '.pkl', 'rb') as f:
        langrec = pickle.load(f)  # загружаем его

    data = ''  # здесь мы очистим и преобразуем входящий текст
    for ch in text:  # берем символ из текста
        if ch not in delim:  # проверяем не разделитель ли это
            data = data + ch  # склеиваем
            data = data.lower()  # все в нижнем регистре
    dict_text = {}  # заводим словарь для подсчета здесь символов
    count = 0  # общее число символов
    for ch in data:
        if ch not in langrec['characters']:  # если буквы нет в словаре
            continue
        count += 1
        if ch in dict_text:
            dict_text[ch] += 1  # если уже встречали этот символ
        else:
            dict_text[ch] = 1  # если еще не встречали этот символ

    for ch in dict_text:
        dict_text[ch] = dict_text[ch] / count  # считаем относительную частоту символа в тексте

    text_vector = []  # создаем вектор
    for ch in langrec['characters']:  # берем очередную букву из всех возможных
        if ch in dict_text:  # если такая буква есть во входящем тексте
            text_vector.append(dict_text[ch])  # добавляем частоту буквы
        else:
            text_vector.append(0.0)  # иначе на этой позиции частота 0
    return text_vector


# функция распознавания языка из строки
def recog(text):
    if text == '':
        return None
    name = 'langrec_monograms'  # имя словаря языков
    with open('obj/' + name + '.pkl', 'rb') as f:
        langrec = pickle.load(f)  # загружаем его

    text_vec = text_to_vec(text)  # берем вектор входящего текста
    text_vec = text_vec / np.linalg.norm(text_vec)  # нормализуем вектор входящего текста
    # для того, чтобы в скалярном произведение мы сразу получили cos

    args = []  # здесь будем хранить результаты скалярного произведения
    for lang_name in langrec['languages']:  # идем по доступным языкам
        vec = langrec[lang_name + '_vector'] / np.linalg.norm(
            langrec[lang_name + '_vector'])  # нормализуем вектор языка
        args.append(np.dot(text_vec, vec))  # добавляем результат скалярного произведения

    # определяем ближайший язык
    proximity = max(args)  # близость к языку
    i_max = args.index(proximity)  # номер ближайшего языка
    i = 0
    for lang_name in langrec['languages']:
        if i_max == i:
            return [lang_name, proximity]
        i += 1
    print('!WARN! recog')
    return args

# функция распознавания языка из файла
def recog_file(file):
    with open(file, 'r') as f:
        text = f.read()
        return recog(text)