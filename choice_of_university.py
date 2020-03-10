from extra import *
import Levenshtein as lv

subjects = {"биология", "иностранный", "история", "математика", "русский", "химия", "география", "информатика", "икт", "литература", "обществознание", "физика", "английский"}
sub_num = {"биология": 3,
           "иностранный": 5,
           "история": 7,
           "математика": 1,
           "русский": 10,
           "химия": 12,
           "география": 4,
           "информатика": 6,
           "икт": 6,
           "литература": 8,
           "обществознание": 9,
           "физика": 11,
           "английский": 5,
           }

active_users = set()


def university_choice(req, res, user):
    if user not in active_users:
        res['response']['text'] = "Какие предметы ты сдаешь на ЕГЭ и какой суммарный балл ты хочешь получить?"
        active_users.add(user)
        return res, UNIVERSITY
    else:
        text = req.json['request']['original_utterance'].split(' ')
        exams = text[:-1]
        points = text[-1]
        confirmed = []
        if not points.isdigit():
            res['response']['text'] = "В конце должен быть назван препдоложительный суммарный балл!"
            return res, UNIVERSITY
        else:
            points = int(points)
        for subject in exams:
            subject = subject.lower()
            if subject in subjects:
                confirmed.append(subject)
            else:
                maxx = (0, '')
                for s in subjects:
                    difference = lv.ratio(subject, s)
                    if difference >= 0.5 and difference > maxx[0]:
                        maxx = (difference, s)
                if maxx[0] > 0:
                    confirmed.append(maxx[1])
        if len(confirmed) < 3:
            res['response']['text'] = "Мало экзаменов или часть введенных не существует"
            return res, UNIVERSITY
        confirmed = set([str(sub_num[subject]) for subject in confirmed])
        result = "https://postupi.online/test/kalkulator-ege/result/?exams="
        result += ';'.join(confirmed)
        result += "&balls="
        mid_points = points // len(confirmed)
        result += ';'.join([str(mid_points) for _ in range(len(confirmed))])
        result += "&fvuz_exam=0"
        res['response']['text'] = result + "\n" + \
                                  "По этой ссылке можно просмотреть подходящие программы бакалавриата." + "\n" + \
                                  "Хочешь узнать еще что-то?"
        active_users.discard(user)
        status = AFTER_TEST
        return res, status
