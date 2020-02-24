import Levenshtein as lv
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


MAKING_CHOICE, CAREER, PROFESSION, UNIVERSITY = "making choice", "профиль", "профессия", "вуз"


def clean_sentence(text, part_of_speech):  # clean sentence from unnecessary words
    part_of_speech = part_of_speech.upper()
    return [word for word in text.split()
         if part_of_speech in morph.parse(word)[0].tag
            or 'UNKN' in morph.parse(word)[0].tag]


def repeat(res):
    res['response']['text'] = "Извините, я вас не понял"
    return res

print(morph.parse('превый')[0].tag)
