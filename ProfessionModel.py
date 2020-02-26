from pony.orm import *


db = Database()


class Professions(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    number = Optional(str)
