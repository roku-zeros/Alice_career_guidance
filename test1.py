from ProfessionModel import *
import requests
import bs4
from extra import *
import Levenshtein as lv


def get_prof_information(link):
    url = requests.get(link)

    b = bs4.BeautifulSoup(url.text, "html.parser")

    url1 = b.select('article')
    information = url1[0].getText()
    university = ' '.join(information.split())
    university = university.split('программы')
    university = [t.rsplit('Бюдж')[0].rsplit('Начало')[0].rsplit('Прох')[0] for t in university if len(t) > 6 and 'в России' not in t
                  and 'профессии' not in t][1:]
    print('\n-------------'.join(university))


print(get_prof_information('https://www.ucheba.ru/prof/204'))