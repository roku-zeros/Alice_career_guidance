import requests
import bs4


def get_prof_information(link):
    url = requests.get(link) #подставляем url

    b = bs4.BeautifulSoup(url.text, "html.parser")

    url1 = b.select('article')
    information = url1[0].getText()

    about = information[information.find('Где работать') + 12:information.find('Компании мечты')]
    company = list(filter(lambda x: x,
                          information[information.find('Компании мечты') + 14:
                                      information.find('Где учиться')].replace('\t', '\n').split('\n')))
    company = ','.join(company) + '.'
    university = information[information.find('Стоимость') + 9:information.find('Интересные ресурсы')].split('программа')
    university = [''.join(list(filter(lambda x: x != '\n' and x != '\t', u))) for u in university][:-1]
    university = ','.join([u[:u.find('Прох')] for u in university])
    return about.replace('\n', '').replace('\xa0', ''), company, university


import csv

FILENAME = "prof.csv"

users_prof = input()

with open(FILENAME, "a", newline="") as file:
    print(users_prof)
    writer = csv.writer(file)
    writer.writerow(users_prof)

with open(FILENAME, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)

