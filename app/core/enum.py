from enum import Enum, unique


@unique
class Gender(Enum):
    FEMALE = "Женщина"
    MALE = "Мужчина"
