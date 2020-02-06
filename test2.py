from flask import Flask, request
import json
import Levenshtein as lv
from random import choice

app = Flask(__name__)

session = {}  # информация о пользователях

tusk_4 = {'банты': 'бАнты',
          'взяла': 'взялА',
          'начатый': 'нАчатый',
          'подняв': 'поднЯв'
        }

tusk_5 = {'бывший путешественник': 'бывалый путешественник',
          'сделать взох': 'сделать вдох',
          'заполнить контейнер': 'наполнить котейнер',
          'враждебная оборона': 'вражеская оборона'
          }

tusk_6 = {'пара туфлей': 'пара туфель',
          'не пророняя': 'не проронив',
          'пара чулков': 'пара чулок',
          'пять блюдцев': 'пять блюдец'
          }


@app.route('/post', methods=['POST'])
def main():
    #создаю ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    user_id = request.json['session']['user_id']
    if user_id not in session:  # если это новый пользователь, то добавляю его в сессию
        session[user_id] = 'choice'
        response['response']['text'] = 'Привет, со мной ты можешь прорешать 4, 5 или 6 ' \
                                       'задание ЕГЭ по русскому языку. Какое задание предпочтешь?'
    else:
        if session[user_id] == 'choice':  # если пользователь выбирает номер
            choice_of_task(request.json, response)
        if session[user_id][0] == '4':
            t4(request.json, response)
            if not session[user_id][1]:
                var = choice(list(tusk_4.keys()))
                session[user_id][1] = [var]
                response['response']['text'] += '\n' + 'Слово: ' + var
            else:
                t4(request.json, response, user_id)
        elif session[user_id][0] == '5':
            t5(request.json, response)
        elif session[user_id][0] == '6':
            t6(request.json, response)
    return json.dumps(response)


def choice_of_task(req, res):
    user_choice = req['request']['original_utterance']
    if user_choice.isalpha():  # преобразую число в цифру, если оно допустимо
        choices = ['четыре', 'пять', 'шесть']
        highet_similarity = [0, 0]  # номер теста и схожесть
        for choice in choices:  # сравниваю с каждым допучтимым чслом
            similarity = lv.ratio(user_choice, choice)
            if similarity > 0.43 and similarity > highet_similarity[1]:
                highet_similarity[0], highet_similarity[1] = choice, similarity
        if highet_similarity[1]:  # если нашлось схожее числительное, то преобразую его в число
            user_choice = choices.index(highet_similarity[0]) + 4
        else:
            user_choice = 0
    user_choice = int(user_choice)
    if user_choice in [4, 5, 6]:
        session[req['session']['user_id']] = [user_choice, '']
        res['response']['text'] = 'Понял, начинаем'
    else:
        res['response']['text'] = 'Я не могу предложить вам это задание'


def t4(req, res, var, user_id):
    answer = req['request']['original_utterance']
    right = tusk_4[session[user_id][1]]
    if answer == right:
        res['response']['text'] = 'Правильно'
    else:
        res['response']['text'] = 'Непарвильно'
    session[user_id][1] = ''


def t5(req, res):
    pass


def t6(req, res):
    pass


if __name__ == '__main__':
    print('START')
    app.run()