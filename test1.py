from pony.orm import *
from SQmodel import *

db.bind(provider='sqlite', filename='professions.db')
db.generate_mapping()

with db_session:
    n1 = HumanType(name='Человек-Природа')
    n1 = HumanType(name='Человек-Техника')
    n1 = HumanType(name='Человек-Человек')
    n1 = HumanType(name='Человек-Знаковая система')
    n1 = HumanType(name='Человек-Художественный образ')
    n1 = ProfessionTarget(name='Гностические профессии')
    n1 = ProfessionTarget(name='Преобразующие профессии')
    n1 = ProfessionTarget(name='Изыскательские профессии')
