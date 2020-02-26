#!/usr/bin/python3
from SQmodel import *
from bs4 import BeautifulSoup
import requests as req
from pony.orm import *
from ProfessionModel import *

db.bind(provider='sqlite', filename='professions_information.db')
db.generate_mapping()


def get_things(text):
    flag = False
    opens = False
    inf = ''
    res = []
    for symb in text:
        if symb == '=':
            flag = True

        if flag and opens:
            if symb == "\"":
                res.append(text)
                text = ''
                opens = False
            else:
                text += symb

        if flag:
            if symb == "\"":
                opens = True
    res2 = []
    for line in res[0].split():
        if 'href' in line:
            res2.append(line[12:-1])
        res2.append(res[-5].replace("\xa0", ""))
    return sorted(list(set(res2)))


while True:
    link = input()[:-1]
    resp = req.get(link)

    soup = BeautifulSoup(resp.text, 'lxml')

    soup = str(soup).split('</a>')[60:-50]

    for i in soup:
        print(get_things(i))
        num, namee = get_things(i)
        if num and namee:

            with db_session:
                print(namee, num)
                new = Profession(name=namee, number=num)

    print(len(soup))
