#!/usr/bin/env python
# coding: utf8
import config as c
import os
import time
import datetime
import ast
import telebot
from random import randint
from configparser import ConfigParser

bot = telebot.TeleBot(c.token)

proxies = {
    'http': 'socks5://telegram.vpn99.net:55655',
    'https': 'socks5://telegram.vpn99.net:55655'
}

curdir = os.path.dirname(os.path.abspath(__file__))
date_format = '%d/%m/%Y'
current_date = datetime.date.today()
current_date = current_date.strftime(date_format)


def stats_read(section, key):  # Парсер results.ini
    result = ConfigParser()
    result.read(curdir + '/results.ini')
    return result.get(section, key)


def stats_record(p):  # Запись статистики в results.ini
    statscheck = ConfigParser()
    statscheck.read(curdir + '/results.ini')
    if not p == "GENERAL":
        if statscheck.has_section(p) is False:
            statscheck.add_section(p)
            with open(curdir + '/results.ini', 'w') as statfile:
                statscheck.write(statfile)
        if statscheck.has_option(p, 'num') is False:
            statscheck.set(p, 'num', "1")
            with open(curdir + '/results.ini', 'w') as statfile:
                statscheck.write(statfile)
        else:
            statscheck.set(p, 'num', str((int(stats_read(p, 'num')) + 1)))
            with open(curdir + '/results.ini', 'w') as statfile:
                statscheck.write(statfile)


def king_stats(line):  # Запись даты и имени топового участника в results.ini по ключу KING
    king_ini = ConfigParser()
    king_ini.read(curdir + '/results.ini')
    king_ini.set('KING', 'data', line)
    with open(curdir + '/results.ini', 'w') as statfile:
        king_ini.write(statfile)


def topchart():  # Построение топа
    l = []
    total = 0
    current_king = ast.literal_eval(stats_read("KING", "data"))
    second = -1  # вспомогательная переменная для выделения второго места
    third = -1  # вспомогательная переменная для выделения третьего места
    first_c = [0, 0]  # 1 позиция для записи доли к общему количеству розыгрышей, 2 счётчик человек в категории
    second_c = [0, 0]  # то же самое для серебряной медали
    third_c = [0, 0]  # то же самое для бронзовой медали

    chart = '<b>' + c.chart_header + '</b>\n'  # Начало построения строки

    plist = ConfigParser()
    plist.read(curdir + '/results.ini')
    for section_name in plist.sections():
        if not section_name == 'KING':
            for (num, count) in plist.items(section_name):
                total += int(count)
                q = [int(count), str(section_name)]
                l.append(q)
    e = sorted(l, key=lambda x: int(x[0]), reverse=True)

    first = e[0][0]

    for item in e:

        if str(item[1]) in current_king and item[0] < first:  # Удаление имен из KING, показатели которых ниже first
            del current_king[item[1]]

        if item[0] == first:  # Первое место (корона)
            if not str(item[1]) in current_king:  # Запись в KING игрока, поднявшегося только что до топа
                date = datetime.date.today()
                current_king[str(item[1])] = date.strftime('%d/%m/%Y')

            first_c[0] = round((int(item[0]) / total) * 100, 2)
            first_c[1] += 1
            daydelta = datetime.datetime.strptime(current_date, date_format) - datetime.datetime.strptime(current_king
                                                                                                          [item[1]],
                                                                                                          date_format)
            daydelta = daydelta.days

            if daydelta is 0:
                days = ' (Сегодня)'
            else:
                days = " (" + str(daydelta) + "д.)"

            chart += u'\U0001F451' + ' ' + str(str(item[1]) + " = " + str(item[0])) + \
                     '<i>' + days + "</i>\n"

        if item[0] < first and (second == -1 or second == item[0]) and third == -1:
            if second == -1:
                second = item[0]

            second_c[0] = round((int(item[0]) / total) * 100, 2)
            second_c[1] += 1

            chart += u'\U0001F948' + ' ' + str(str(item[1]) + " = " + str(item[0])) + "\n"

        if item[0] < second and (third == -1 or third == item[0]):
            if third == -1:
                third = item[0]

            third_c[0] = round((int(item[0]) / total) * 100, 2)
            third_c[1] += 1

            chart += u'\U0001F949' + ' ' + str(str(item[1]) + " = " + str(item[0])) + "\n"

        if item[0] < third:
            chart += str(str(item[1]) + " = " + str(item[0])) + "\n"
    # Подвал сообщения с топом. Раскомментируйте необходимую часть для более тонкой статистики.
    chart += '<code>======\n' + c.chart_total_phrase + ' ' + str(total) + '\n</code>'
    '''\nДоля выпаданий на участника:\n' +\
             u'\U0001F451' + ': ' + str(first_c[0]) + '%\n' + \
             u'\U0001F948' + ': ' + str(second_c[0]) + '%\n' + \
             u'\U0001F949' + ': ' + str(third_c[0]) + '%\n' + \
             u'\u2211' + ' выпаданий на группу:\n' + \
             u'\U0001F451' + ': ' + str(first_c[0] * first_c[1]) + '%\n' + \
             u'\U0001F948' + ': ' + str(second_c[0] * second_c[1]) + '%\n' + \
             u'\U0001F949' + ': ' + str(third_c[0] * third_c[1]) + '%\n</code>'''
    king_stats(str(current_king))
    return chart


def sendtotg(text):
    bot.send_message(c.chatid, parse_mode='html', text=text)


winner = c.participants[randint(0, len(c.participants) - 1)]
startphrase = c.startphrase[randint(0, len(c.startphrase) - 1)]
searchphrase = c.searchphrase[randint(0, len(c.searchphrase) - 1)]
foundphrase = str(c.foundphrase[randint(0, len(c.foundphrase) - 1)])
if "%" in foundphrase:
    foundphrase = str(foundphrase % winner)

stats_record(winner)

sendtotg(startphrase)
time.sleep(randint(1, 2))
sendtotg(searchphrase)
time.sleep(randint(1, 3))
sendtotg(foundphrase)
sendtotg(topchart())
