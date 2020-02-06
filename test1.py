import pymorphy2
morph = pymorphy2.MorphAnalyzer()

word = "стали"
p = morph.parse(word)[0].tag  # Делаем полный разбор, и берем первый вариант разбора (условно "самый вероятный", но не факт что правильный)
if 'VERB' in p:
    print(p)