#!/usr/bin/env python
# coding: utf8
import config as c
import os
import time
import datetime
import ast
from random import randint
from configparser import ConfigParser


curdir = os.path.dirname(os.path.abspath(__file__))
date_format = '%d/%m/%Y'
curdate = datetime.date.today()
curdate = curdate.strftime('%d/%m/%Y')


def resultsread(section, key):  # Парсер results.ini
    result = ConfigParser()
    result.read(curdir + '/results.ini')
    return result.get(section, key)


def stats(p):  # Запись статистики
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
            statscheck.set(p, 'num', str((int(resultsread(p, 'num')) + 1)))
            with open(curdir + '/results.ini', 'w') as statfile:
                statscheck.write(statfile)


def kingstats(line):
    kingini = ConfigParser()
    kingini.read(curdir + '/results.ini')
    kingini.set('KING', 'data', line)
    with open(curdir + '/results.ini', 'w') as statfile:
        kingini.write(statfile)


def topchart():  # Построение топа
    chart = '<b>====== ТОП пидоров ======</b>\n'
    l = []
    curking = ast.literal_eval(resultsread("KING", "data"))
    plist = ConfigParser()
    plist.read(curdir + '/results.ini')
    total = 0
    for section_name in plist.sections():
        if not section_name == 'KING':
            for(num, count) in plist.items(section_name):
                total += int(count)
                q = [int(count), str(section_name)]
                l.append(q)
    e = sorted(l, key=lambda x: int(x[0]), reverse=True)
    best = e[0][0]
    second = -1
    third = -1
    first_c = [0, 0]
    second_c = [0, 0]
    third_c = [0, 0]
    for item in e:

        if str(item[1]) in curking and item[0] < best:
            del curking[item[1]]

        if item[0] == best:
            if not str(item[1]) in curking:
                date = datetime.date.today()
                curking[str(item[1])] = date.strftime('%d/%m/%Y')
            first_c[0] = round((int(item[0])/total)*100, 2)
            first_c[1] += 1
            daydelta = datetime.datetime.strptime(curdate, date_format) - datetime.datetime.strptime(curking[item[1]], date_format)
            daydelta = daydelta.days
            if daydelta is 0:
                days = ' (Сегодня)'
            else:
                days = " (" + str(daydelta) + "д.)"
            chart = chart + u'\U0001F451' + ' ' + str(str(item[1]) + " = " + str(item[0])) + days + "\n"

        if item[0] < best and (second == -1 or second == item[0]) and third == -1:
            if second == -1:
                second = item[0]
            chart = chart + u'\U0001F948' + ' ' + str(str(item[1]) + " = " + str(item[0])) + "\n"
            second_c[0] = round((int(item[0]) / total) * 100, 2)
            second_c[1] += 1
        if item[0] < second and (third == -1 or third == item[0]):
            if third == -1:
                third = item[0]
            chart = chart + u'\U0001F949' + ' ' + str(str(item[1]) + " = " + str(item[0])) + "\n"
            third_c[0] = round((int(item[0]) / total) * 100, 2)
            third_c[1] += 1
        if item[0] < third:
            chart = chart + str(str(item[1]) + " = " + str(item[0])) + "\n"
    chart += '<code>======\nПопаданий из пидормёта: ' + str(total) + \
             '\nДоля попаданий на пидора:\n' +\
             u'\U0001F451' + ': ' + str(first_c[0]) + '%\n' + \
             u'\U0001F948' + ': ' + str(second_c[0]) + '%\n' + \
             u'\U0001F949' + ': ' + str(third_c[0]) + '%\n' + \
             u'\u2211' + ' попаданий на группу:\n' + \
             u'\U0001F451' + ': ' + str(first_c[0] * first_c[1]) + '%\n' + \
             u'\U0001F948' + ': ' + str(second_c[0] * second_c[1]) + '%\n' + \
             u'\U0001F949' + ': ' + str(third_c[0] * third_c[1]) + '%\n</code>'
    kingstats(str(curking))
    return chart


def sendtotg(text):
    os.system('curl -s -X POST https://api.telegram.org/bot' + c.token + '/sendMessage -d chat_id=' + c.chatid +
              ' -d parse_mode=html -d text="' + str(text) + '"')


pidor = c.pidors[randint(0, len(c.pidors)-1)]
startphrase = c.startphrase[randint(0, len(c.startphrase)-1)]
searchphrase = c.searchphrase[randint(0, len(c.searchphrase)-1)]
foundphrase = str(c.foundphrase[randint(0, len(c.foundphrase)-1)] % pidor)


stats(pidor)

sendtotg(startphrase)
time.sleep(randint(1, 3))
sendtotg(searchphrase)
time.sleep(randint(1, 3))
sendtotg(foundphrase)
sendtotg(topchart())
