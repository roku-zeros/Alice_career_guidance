from pony.orm import *
from SQmodel import *

db.bind(provider='sqlite', filename='Professions.db')
db.generate_mapping()

with db_session:
    for prof in select(p for p in Profession):
        print(prof.human_type.id)
