import Levenshtein as lv
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def clean_sentence(text, part_of_speech):  # clean sentence from unnecessary words
    part_of_speech = part_of_speech.upper()
    return [word for word in text.split()
         if part_of_speech in morph.parse(word)[0].tag]


def making_choice(req, res, user):
    choices = ['профиль', 'универститет', 'профессия']
    max_similarity = [-1.0, '']  # similarity and word
    text = clean_sentence(req, 'noun')
    for i in range(len(choices)):
        for word in text:
            similarity = lv.ratio(choices[i], word)
            if similarity > max_similarity[0]:
                max_similarity = [similarity, choices[i]]
    print(max_similarity[1])


print(clean_sentence('вущ', 'noun'))
print(morph.parse('вущ')[0].tag)
