from pony.orm import *


db = Database()


class Profession(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    number = Optional(str)
