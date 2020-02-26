from ProfessionModel import *
import requests
import bs4
from extra import *
import Levenshtein as lv

db.bind(provider='sqlite', filename='professions_information.db')
db.generate_mapping()

active_users = set()


def profession_choice(req, res, user):
    if user not in active_users:
        res['response']['text'] = "О какой профессии вы хотите узнать больше?"
        active_users.add(user)
        return res
    else:
        users_prof = req.json['request']['original_utterance']
        with db_session:
            max_similarity = [0, '', '']
            for prof in select(p for p in Profession):
                similarity = lv.ratio(prof.name, users_prof)
                if similarity > max_similarity[0]:
                    max_similarity = [similarity, prof.name, prof.number]
            if max_similarity[0] < 0.45:
                res['response']['text'] = "Я пока не знаю этой профессии, она скоро бует добавлена. Попробуйте назвать другую."
                return res
            choosen_prof = max_similarity[1], max_similarity[2]
            link = "https://www.ucheba.ru/prof/" + choosen_prof[1]
            about, company, university = get_prof_information(link)
            answer = choosen_prof[0] + '\n' + \
                     "Про работу: " + about + '\n' + \
                     "Подходящие компагии: " + company + '\n' +\
                     "Подходящие учебные заведения: " + university + "." + "\n" + "Хотите узнать еще что-то?"
            res['response']['text'] = answer
            status = AFTER_TEST
            active_users.discard(user)
            return res, status


def get_prof_information(link):
    url = requests.get(link)

    b = bs4.BeautifulSoup(url.text, "html.parser")

    url1 = b.select('article')
    information = url1[0].getText()

    about = information[information.find('Где работать') + 12:information.find('Компании мечты')]
    company = list(filter(lambda x: x,
                          information[information.find('Компании мечты') + 14:
                                      information.find('Где учиться')].replace('\t', '\n').split('\n')))
    company = ','.join(company) + '.'
    university = information[information.rfind('Где учиться') + 11:]
    #university = [''.join(list(filter(lambda x: x != '\n' and x != '\t', u))) for u in university][:-1]
    #university = ','.join([u[:u.find('Прох')] for u in university])
    university = ' '.join(information.split())
    university = university.split('программы')
    university = [t.rsplit('Бюдж')[0].rsplit('Начало')[0].rsplit('Прох')[0] for t in university if
                  len(t) > 6 and 'в России' not in t and 'профессии' not in t][1:]
    return about.replace('\n', '').replace('\xa0', ''), company, ','.join(university)
