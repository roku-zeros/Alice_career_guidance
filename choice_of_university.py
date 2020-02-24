from main import session
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


def choice_of_university(req, res, user):
    if user not in active_users:
        res['response']['text'] =  "Какие предметы ты садешь на егэ и какой суммарный балл ты хочешь получить?"
        active_users.add(user)
        return res
    else:
        text = req.json['request']['original_utterance'].split(' ')
        exams = text[:-1]
        points = text[-1]
        confirmed = []
        if not points.isdigit():
            res['response']['text'] = "В конце должен быть назван препдоложительный суммарный балл!"
            return res
        else:
            points = int(points)
        for subject in exams:
            subject = subject.lower()
            if subject in subjects:
                confirmed.append(subject)
            else:
                maxx = (0, '')
                for s in subjects:
                    difference = lv.ratio(subjects, s)
                    if difference >= 0.5 and difference > maxx[0]:
                        maxx = (s, difference)
                if maxx[0] > 0:
                    confirmed.append(maxx[1])
        if len(confirmed) < 3:
            res['response']['text'] = "Мало экзаменов или часть введенных не существует"
            return res
        print(confirmed)
        print([str(sub_num[subject]) for subject in confirmed])
        confirmed = set([str(sub_num[subject]) for subject in confirmed])
        result = "https://postupi.online/test/kalkulator-ege/result/?exams="
        result += ';'.join(confirmed)
        result += "&balls="
        mid_points = points // len(confirmed)
        result += ';'.join([str(mid_points) for _ in range(len(confirmed))])
        result += "&fvuz_exam=0"
        res['response']['text'] = result + "\n" + "По этой ссылке просмотреть подходящие программы бакалавриата."
        active_users.discard(user)
        return res
