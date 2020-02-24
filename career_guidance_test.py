from flask import Flask, request
from extra import *
import json
import Levenshtein as lv

READY = "ready"

main_questions = {1: ["Ухаживать за животными",
                      "Обслуживать машины, приборы (следить, регулировать)"],
             2: ["Помогать больным ",
                 "Составлять таблицы, схемы, программы для вычислительных машин"],
             3: ["Следить за качеством книжных иллюстраций, плакатов, художественных открыток, грампластинок ",
                 "Следить за состоянием, развитием растений"],
             4: ["Обрабатывать материалы (дерево, ткань, металл, пластмассу и т.п.) ",
                 "Доводить Товары до потребителя, рекламировать, продавать"],
             5: ["Обсуждать научно-популярные книги, статьи",
                 "Обсуждать художественные книги (или пьесы, концерты)"],
             6: ["Выращивать молодняк (животных какой-либо породы)",
                 "Тренировать товарищей (или младших) в выполнении каких-либо действий (трудовых, учебных, спортивных)"],
             7: ["Копировать рисунки, изображения (или настраивать музыкальные инструменты)",
                 "Управлять каким-либо грузовым (подъемным или транспортным) средством – подъемным краном, трактором, тепловозом и др."],
             8: ["Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.)",
                 "Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)"],
             9: ["Ремонтировать вещи, изделия (одежду, технику), жилище",
                 "Искать и исправлять ошибки в текстах, таблицах, рисунках"],
             10: ["Лечить животных ",
                  "Выполнять вычисления, расчеты"],
             11: ["Выводить новые сорта растений",
                  "Конструировать, проектировать новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.)"],
             12: ["Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять ",
                  "Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок)"],
             13: ["Наблюдать, изучать работу кружков художественной самодеятельности",
                  "Наблюдать, изучать жизнь микробов"],
             14: ["Обслуживать, налаживать медицинские приборы, аппараты ",
                  "Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п."],
             15: ["Художественно описывать, изображать события (наблюдаемые и представляемые)",
                  "Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др."],
             16: ["Делать лабораторные анализы в больнице",
                  "Принимать, осматривать больных, беседовать с ними, назначать лечение"],
             17: ["Красить или расписывать стены помещений, поверхность изделий ",
                  "Осуществлять монтаж или сборку машин, приборов"],
             18: ["Организовать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п. ",
                  "Играть на сцене, принимать участие в концертах"],
             19: ["Изготовлять по чертежам детали, изделия (машины, одежду), строить здания",
                  "Заниматься черчением, копировать чертежи, карты"],
             20: ["Вести борьбу с болезнями растений, с вредителями леса, сада",
                  "Работать на клавишных машинах (пишущей машинке, телетайпе, наборной машине и др.)"]
             21: """Выбери числа от 1 до 3, соответствующие подходящим классам профессий:
             1) Гностический - направлен на сортировку, сравнивание, проверку и оценивание. Примеры: биолог-лаборант, корректор, социолог.
             2) Преобразовательный  - направлен на преоброзование энергии, информации, предметы, процессы. Примеры: расстенивод, учитель, бухгалтер.
             3) Изыскательские - напрвлен на создание чего-либо нового. Примеры: программист, инженер, биолог-исследователь, дизайнер."""
             }

extra_questions = {}  ############

HUMAN_NATURE = [main_questions[1][0], main_questions[3][1], main_questions[6][0], main_questions[10][0], main_questions[11][0], main_questions[13][1], main_questions[16][0], main_questions[20][0]]
HUMAN_TECHNIC = [main_questions[1][1], main_questions[4][0], main_questions[7][1], main_questions[9][0], main_questions[11][1], main_questions[14][0], main_questions[17][1], main_questions[19][0]]
HUMAN_HUMAN = [main_questions[2][0], main_questions[4][1], main_questions[6][1], main_questions[8][0], main_questions[12][0], main_questions[14][1], main_questions[16][1], main_questions[18][0]]
HUMAN_SIGN_SYSTEM = [main_questions[2][1], main_questions[5][0], main_questions[9][1], main_questions[10][1], main_questions[12][1] ,main_questions[15][0], main_questions[19][1], main_questions[20][1]]
HUMAN_ARTISTIC_IMAGE = [main_questions[3][0], main_questions[5][1], main_questions[7][0], main_questions[8][0], main_questions[13][0], main_questions[15][1], main_questions[17][0], main_questions[18][1]]
HUMAN_TYPES = [HUMAN_NATURE, HUMAN_TECHNIC, HUMAN_HUMAN, HUMAN_SIGN_SYSTEM, HUMAN_ARTISTIC_IMAGE]

users_careers = {}  # information about users and theirs career


def career_guidance_test(req, res, user):
    if user in users_careers:  # ask new question
        users_question = users_careers[user][0]
        if not add_choice(req, res, user, users_question) and users_question <= 20:  # adding users choice
            res['response']['text'] = "Отвечать нужно один или два!"
            return res
        if users_question <= 20:
            users_question = users_careers[user][0]
            res['response']['text'] = (main_questions[users_question][0] + ' или ' + main_questions[users_question][1] + '?')
            users_careers[user][0] += 1
        elif users_question == 21:
            add_last_choice()
        else:  # generate tests result
            test_result(req, res, user)
        return res
    else:
        res['response']['text'] = "Чтобы пройти тест, нужно будет выбирать между первой и второй работой, отвечая один или два соответсвенно." \
                                  "Ухаживать за животными или Обслуживать машины, приборы (следить, регулировать)"
        users_careers[user] = [2, [0, 0, 0, 0, 0], '']  # question, points, profession target


def add_choice(req, res, user, question):
    text = req.json['request']['original_utterance']
    if text.lower() == 'один' or text == '1':
        choice = main_questions[question][0]
    elif text.lower() == 'два' or text == '2':
        choice = main_questions[question][0]
    else:
        res['response']['text'] = "Отвечать нужно один или два!"
        return False
    for type in range(len(HUMAN_TYPES)):
        if choice in HUMAN_TYPES[type]:
            users_careers[user][1][type] += 1
    return True


def add_last_choice(req, res, user):
    text = req.json['request']['original_utterance']
    choices = []
    for word in text.split():
        if text.lower() == 'один' or text == '1':
            choices.append(1)
        elif text.lower() == 'два' or text == '2':
            choices.append(2)
        elif text.lower() == 'три' or text == '3':
            choices.append(3)
    if not choices:
        res['response']['text'] = "Отвечать нужно один или два, или три!"
        return False
    users_careers[user][3] = choices
    return True


def test_result(res, req, user):
    pass
