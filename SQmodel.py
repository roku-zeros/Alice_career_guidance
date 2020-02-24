from pony.orm import *


db = Database()


class Profession(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    human_type = Required('HumanType')
    profession_target = Required('ProfessionTarget')


class HumanType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    professions = Set(Profession)


class ProfessionTarget(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    professions = Set(Profession)
