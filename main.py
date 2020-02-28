from flask import Flask, request
import json
from career_guidance_test import *
from choice_of_university import university_choice
from professions_choice import profession_choice
import Levenshtein as lv


session = {}  # информация о пользователях

morph = pymorphy2.MorphAnalyzer()

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    result = ''
    text = request.json['request']['original_utterance']
    user_id = request.json['session']['user_id']  # get user id
    if user_id not in session:  # if it's new user
        greeting(response, user_id)
    elif session[user_id] == 'start':
        if text.lower() == 'да' or text.lower() == 'хочу':
            start(response, user_id)
        elif text.lower() == 'нет':
            response['response']['text'] = "До новых встреч"
        else:
            repeat(response)
    elif session[user_id] == AFTER_TEST:
        text = text.lower()
        if "да" in text:
            session[user_id] = MAKING_CHOICE
            response['response']['text'] = "Университет? Профессия? Профиль? О чем ты еще хочешь узнать?"
        elif "нет" in text:
            response['response']['text'] = "До новых встреч"
            response['response']['end_session'] = True
        else:
            repeat(response)
    elif session[user_id] == MAKING_CHOICE:
        making_choice(text.lower(), response, user_id)
    elif session[user_id] == CAREER:
        result = career_guidance_test(request, response, user_id)
        if AFTER_TEST in result:
            print('!!!!!!!!!')
            session[user_id] = AFTER_TEST
    elif session[user_id] == UNIVERSITY:
        result = university_choice(request, response, user_id)
    elif session[user_id] == PROFESSION:
        result = profession_choice(request, response, user_id)
    if AFTER_TEST in result:
        session[user_id] = AFTER_TEST
    return json.dumps(response)


def greeting(res, user):  # greeting and adding to the session
    session[user] = 'start'
    res['response']['text'] = "Привет! Вы хотите узнать больше про вуз, профессию или выбрать профиль?"


def start(res, user):  # ask what user want
    session[user] = MAKING_CHOICE
    res['response']['text'] = "Я могу помочь с выбором профиля, университета или " \
                              "же профессии. Что тебя интересует?"


def making_choice(req, res, user):
    choices = ['профиль', 'универститет', 'вуз', 'профессия']
    choices_const = [CAREER, UNIVERSITY, UNIVERSITY, PROFESSION]
    max_similarity = [-1.0, '', '']  # similarity and word
    text = clean_sentence(req, 'noun')
    for i in range(len(choices)):
        for word in text:
            similarity = lv.ratio(choices[i], word)
            if similarity > max_similarity[0]:
                max_similarity = [similarity, choices[i], choices_const[i]]
    if max_similarity[0] > 0.3:
        session[user] = max_similarity[2]

        if session[user] == CAREER:
            career_guidance_test(request, res, user)
        elif session[user] == UNIVERSITY:
            university_choice(request, res, user)
        elif session[user] == PROFESSION:
            profession_choice(req, res, user)

    else:
        repeat(res)


if __name__ == '__main__':
    print('START')
    app.run(host='0.0.0.0', port=5000)

