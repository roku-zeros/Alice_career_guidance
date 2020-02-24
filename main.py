from flask import Flask, request
import json
import Levenshtein as lv
import pymorphy2
from extra import *
from career_guidance_test import *
from choice_of_university import *


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
    text = request.json['request']['original_utterance']
    user_id = request.json['session']['user_id']  # get user id
    if user_id not in session:  # if it's new user
        greeting(response, user_id)
    elif session[user_id] == 'start':
        if text.lower() == 'да':
            start(response, user_id)
        elif text.lower() == 'нет':
            response['response']['text'] = 'Пока'
        else:
            repeat(response)
    elif session[user_id] == MAKING_CHOICE:
        making_choice(text.lower(), response, user_id)
    elif session[user_id] == CAREER:
        career_guidance_test(request, response, user_id)
    elif session[user_id] == UNIVERSITY:
        choice_of_university(request, response, user_id)
    elif session[user_id] == PROFESSION:
        pass
    return json.dumps(response)


def greeting(res, user):  # greeting and adding to the session
    session[user] = 'start'
    res['response']['text'] = "Привет! Перед тобой встал сложный выбор и " \
                              "тебе нужно помочь выбрать профиль, профессию или вуз?"


def start(res, user):  # ask what user want
    session[user] = MAKING_CHOICE
    res['response']['text'] = "Я могу помочь с выбором профиля, университета или " \
                              "же профессии, если ты выбрал профиль. Что тебя интересует?"


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
    print(max_similarity)
    if max_similarity[0] > 0.35:
        session[user] = max_similarity[2]

        if session[user] == CAREER:
            career_guidance_test(request, res, user)
        elif session[user] == UNIVERSITY:
            choice_of_university(request, res, user)
        elif session[user] == PROFESSION:
            pass

    else:
        repeat(res)


if __name__ == '__main__':
    print('START')
    app.run()
