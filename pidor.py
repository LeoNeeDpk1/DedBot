#!/usr/bin/env python
# coding: utf8
import config as c
import os
import time
from random import randint
from configparser import ConfigParser


curdir = os.path.dirname(os.path.abspath(__file__))


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


def topchart():
    chart = '<b>=== ТОП пидоров ===</b>\n'
    l = []
    plist = ConfigParser()
    plist.read(curdir + '/results.ini')
    for section_name in plist.sections():
        for(num, count) in plist.items(section_name):
            q = [int(count), str(section_name)]
            l.append(q)
    e = sorted(l, key=lambda x: str(x[0]), reverse=True)
    best = e[0][0]
    for item in e:
        if item[0] == best:
            chart = chart + str(str(item[1]) + " = " + str(item[0])) + " " + u'\U0001F451' + "\n"
        else:
            chart = chart + str(str(item[1]) + " = " + str(item[0])) + "\n"
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
