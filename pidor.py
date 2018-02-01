#!/usr/bin/env python
# coding: utf8
import config
import os
import time
from random import randint
from configparser import ConfigParser





curdir = os.path.dirname(os.path.abspath(__file__))





def resultsread(section, key):  # Парсер results.ini
    result = ConfigParser()
    result.read('/home/fku-server/pidor_roulette/results.ini')
    return result.get(section, key)


def stats(p): #Запись статистики
    statscheck = ConfigParser()
    statscheck.read('/home/fku-server/pidor_roulette/results.ini')
    if not p == "GENERAL":
        if statscheck.has_section(p) == False:
            statscheck.add_section(p)
            with open('/home/fku-server/pidor_roulette/results.ini', 'w') as statfile:
                statscheck.write(statfile)
        if statscheck.has_option(p, 'num') == False:
            statscheck.set(p,'num',"1")
            with open('/home/fku-server/pidor_roulette/results.ini', 'w') as statfile:
                statscheck.write(statfile)
        else:
            statscheck.set(p,'num', (int(resultsread(p, 'num'))+ 1))
            with open('/home/fku-server/pidor_roulette/results.ini', 'w') as statfile:
                statscheck.write(statfile)

def topchart():
    lastsection = ""
    t = ""
    l = []
    plist = ConfigParser()
    plist.read('/home/fku-server/pidor_roulette/results.ini')
    for section_name in plist.sections():
        for(num, count) in plist.items(section_name):
            q = [int(count), str(section_name)]
            l.append(q)
    e = sorted(l, key=lambda x: str(x[0]), reverse=True)
    for item in e:
        t = t + str(str(item[1]) + " = " + str(item[0])) + "\n"
    return t

with open('/home/fku-server/pidor_roulette/pidors') as p:
    plines = p.read().split(',')
with open('/home/fku-server/pidor_roulette/quotes') as q:
    qlines = q.read().split('*')
with open('/home/fku-server/pidor_roulette/quotes2') as q2:
    q2lines = q2.read().split('*')

quote = qlines[randint(0, len(qlines)-1)]
quote2 = q2lines[randint(0, len(q2lines)-1)]
pidor = plines[randint(0, len(plines)-1)]

pidor = str(pidor).replace("\n", "")
stats(str(pidor))

'''os.system('curl -s -X POST https://api.telegram.org/bot/sendMessage -d chat_id= -d text="' + str(quote) + '"')
time.sleep(randint(1, 3))
os.system('curl -s -X POST https://api.telegram.org/bot/sendMessage -d chat_id= -d text="' + str(quote2) + '"')
time.sleep(randint(1, 3))
os.system('curl -s -X POST https://api.telegram.org/bot/sendMessage -d chat_id= -d parse_mode=html -d text="Пидор обнаружен! И это: <b>' + str(pidor) + '</b>"')
os.system('curl -s -X POST https://api.telegram.org/bot/sendMessage -d chat_id= -d parse_mode=html -d text="<b> Доска позора:</b>\n' + str(topchart()) + '"')
'''






























