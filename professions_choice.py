from main import session
from extra import *
import Levenshtein as lv
from ProfessionModel import *

db.bind(provider='sqlite', filename='professions_information.db')
db.generate_mapping()

active_users = set()


def profession_choice(req, res, user):
    if user not in active_users:
        res['response']['text'] = "О какой профессии ты хочешь узнать больше"
        return res
    else:
        users_prof = req['request']['original_utterance']
        max_similarity = [0, '', '']
        with db_session:
            for prof in select(p for p in Professions):
                similarity = lv.ratio(prof.name, users_prof)
                if similarity > max_similarity[0]:
                    max_similarity = [similarity, prof.name, prof.nuber]

