from pony.orm import *
from SQmodel import *

db.bind(provider='sqlite', filename='Professions.db')
db.generate_mapping()

with db_session:
    for prof in select(p for p in Profession):
        print(prof.name)


import requests
import bs4


def get_prof_information(link):
    url = requests.get('https://www.ucheba.ru/prof/1577') #подставляем url

    b = bs4.BeautifulSoup(url.text, "html.parser")

    url1 = b.select('article')
    url_print = url1[0].getText()
    text = url_print.replace('\t', '').replace('\n', '').split(' ')
    text = ' '.join(list(filter(lambda x: x, text)))
    text = text.split('.')

    for i in text:
        print(i)
        print('--------------')
    text = '.'.join(text)
    print(text)
    about = text[text.find('Где работать') + 12:text.find('Компании мечты')]
    print('------')
    print(about)
    company = text[text.find('Компании мечты') + 14:text.find('Где учиться')]
    print(url_print)


get_prof_information(12)
