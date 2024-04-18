from enum import Enum


class SurveyQuestions(str, Enum):
    age = 'Введите возраст'
    consent = 'Вы готовы ответить на несколько вопросов?'
    email = 'Введите электронную почту'
    gender = 'Выберите пол'
    height = 'Введите рост в см'
    physical_activity = (
        'Выберите фразу, наиболее точно описывающую вашу'
        ' физическую активность'
    )
    purpose = 'Выберите цель'
    weight = 'Введите вес в кг'


CONFIRM = (
    ('YES', 'Да'),
    ('NO', 'Нет'),
)
GENDER = (
    ('MALE', 'Мужчина'),
    ('FAMALE', 'Женщина'),
)
PHYSICAL_ACTIVITY = (
    ('ABSENT', 'Отсутствует'),
    ('INFREQUENT', 'Редкие тренировки'),
    ('MODERATE', 'Умеренная активность'),
    ('INTENSE', 'Интенсивные тренировки'),
    ('PROFESSIONAL', 'Профессиональный спорт'),
)

ACTIVITY_PURPOSE = (
    ('GO_SLIM', 'Сброс массы'),
    ('KEEP_LEVEL', 'Поддержание массы'),
    ('ADD_MASS', 'Набор массы'),
)

AM_NOON_PM = (
    ('AM', '11:00'),
    ('NOON', '14:00'),
    ('PM', '19:00'),
)

WORKOUT_TYPE = (
    ('Cardio', 'Кардио'),
    ('Legs', 'Ноги'),
    ('Back', 'Спина, плечи, трицепс'),
    ('Front', 'Грудь, бицепс'),
)

INTRO_SURVEY_TEXT = '<b>Здесь будет мотивирующие введение.</b>\n😜\n'

ALLOWED_AGE_RANGE = (14, 55)
ALLOWED_HEIGHT_RANGE = (100, 250)
ALLOWED_WEIGHT_RANGE = (20, 500)

PHYS_ACTIV_KOEF = {
    'ABSENT': 1.2,
    'INFREQUENT': 1.375,
    'MODERATE': 1.55,
    'INTENSE': 1.725,
    'PROFESSIONAL': 1.9,
}

WEIGHT_COEF_MAN = 13.4
WEIGHT_COEF_WOMAN = 9.2
HEIGHT_COEF_MAN = 4.8
HEIGHT_COEF_WOMAN = 3.1
AGE_COEF_MAN = 5.7
AGE_COEF_WOMAN = 4.3
CAL_COEF_MAN = 88.36
CAL_KOEF_WOMAN = 447.6
COEF_TO_SLIM = 0.85
COEF_ADD_MASS = 1.2
COEF_ROUND = 2
