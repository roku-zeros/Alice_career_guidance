from flask import Flask, request
import json
import Levenshtein as lv
import pymorphy2


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
    elif session[user_id] == 'making choice':
        making_choice(text.lower(), response, user_id)
    elif session[user_id] == 'профиль':
        pass
    elif session[user_id] == 'универститет' or session[user_id] == 'вуз':
        pass
    elif session[user_id] == 'профессия':
        pass
    return json.dumps(response)


def greeting(res, user):  # greeting and adding to the session
    session[user] = 'start'
    res['response']['text'] = "Привет! Перед тобой встал сложный выбор и " \
                              "тебе нужно помочь выбрать профиль, профессию или вуз?"


def start(res, user):  # ask what user want
    session[user] = 'making choice'
    res['response']['text'] = "Я могу помочь с выбором профиля, университета или " \
                              "же профессии, если ты выбрал профиль. Что тебя интересует?"


def making_choice(req, res, user):
    choices = ['профиль', 'универститет', 'вуз', 'профессия']
    max_similarity = [-1.0, '']  # similarity and word
    text = clean_sentence(req, 'noun')
    for i in range(len(choices)):
        for word in text:
            similarity = lv.ratio(choices[i], word)
            if similarity > max_similarity[0]:
                max_similarity = [similarity, choices[i]]
    print(max_similarity)
    if max_similarity[0] > 0.35:
        session[user] = max_similarity[1]
    else:
        repeat(res)


def clean_sentence(text, part_of_speech):  # clean sentence from unnecessary words
    part_of_speech = part_of_speech.upper()
    return [word for word in text.split()
         if part_of_speech in morph.parse(word)[0].tag
            or 'UNKN' in morph.parse(word)[0].tag]


def repeat(res):
    res['response']['text'] = "Извините, я вас не понял"
    return res


if __name__ == '__main__':
    print('START')
    app.run()
