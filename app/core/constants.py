from enum import Enum


class SurveyQuestions(str, Enum):
    AGE = 'Введите возраст'
    CONSENT = 'Вы готовы ответить на несколько вопросов?'
    EMAIL = 'Введите электронную почту'
    GENDER = 'Выберите пол'
    HEIGHT = 'Введите рост в см'
    PHYSICAL_ACTIVITY = (
        'Выберите фразу, наиболее точно описывающую вашу'
        ' физическую активность'
    )
    PURPOSE = 'Выберите цель'
    WEIGHT = 'Введите вес в кг'


ACTIVITY_KEYBOARD_SIZE = (1,)
ACTIVITY_PURPOSE = (
    ('GO_SLIM', 'Сброс массы'),
    ('KEEP_LEVEL', 'Поддержание массы'),
    ('ADD_MASS', 'Набор массы'),
)
AGE_COEF_MAN = 5.7
AGE_COEF_WOMAN = 4.3
ALLOWED_AGE_RANGE = (14, 55)
ALLOWED_HEIGHT_RANGE = (100, 250)
ALLOWED_WEIGHT_RANGE = (20, 500)
AM_NOON_PM = (
    ('AM', '11:00'),
    ('NOON', '14:00'),
    ('PM', '19:00'),
)

BACK = 'Назад👈'
BUTTONS = {'Сон💤': 'sleep', 'Питание🥦': 'diet', 'Тренировки🏋‍♂️': 'workouts'}
CAL_COEF_MAN = 88.36
CAL_KOEF_WOMAN = 447.6
COEF_TO_SLIM = 0.85
COEF_ADD_MASS = 1.2
COEF_ROUND = 2
CAPTIONS = {
    'main': 'Добро пожаловать в Ваш личный помощник самосовершенствования.',
    'workouts': '<b>Какой вид тренировки предпочитаете?</b>',
    'diet': 'Ваша норма калорий на день {} Ккал',
    'oops': {
        1: 'В данный момент для Вас нет тренировки...',
        2: 'В данный момент для Вас нет упражнений к этой тренировке...',
    },
}
COEF_TO_SLIM = 0.85
COEF_ADD_MASS = 1.2
COEF_ROUND = 2
CONFIRM = (
    ('YES', 'Да'),
    ('NO', 'Нет'),
)
COMPLETE = 'Завершить⛔️'
COURSE = 'course'
DEFAULT_KEYBOARD_SIZE = (2,)
DIET = 'diet'

EXERCISE = 'exercise'
EXERCISE_WORKOUT = 'exercise_workout'

FMT_JPG = '.jpg'

GENDER = (
    ('MALE', 'Мужчина'),
    ('FEMALE', 'Женщина'),
)

HASH_PASSWORD = 'nkajipfncu89288)*&^guyb'
HEIGHT_COEF_MAN = 4.8
HEIGHT_COEF_WOMAN = 3.1

INTRO_SURVEY_TEXT = '<b>Здесь будет мотивирующие введение.</b>\n😜\n'
INVALID_NUM_MESSAGE = (
    'Введите целое число в диапазоне от {} до {} включительно'
)
INVALID_EMAIL_MESSAGE = 'Ошибка при вводе email. Попробуйте снова.'
INVALID_LITERAL_ERROR = (
    'Переданную строку "{}" не возможно преобразовать в целое число.'
)

MAIN_MENU = 'main'
MOSCOW = 'Europe/Moscow'

NEXT = 'След. ➡️'

OUT_OF_ALLOWED_RANGE_ERROR = (
    'Введенное число {} не принадлежит диапазону {} - {} включительно.'
)


KB_TEXT_FOR_DIET = 'Контроль Калорий!'
KB_TEXT_FOR_TRAINING = 'К тренировкам!'
KB_TEXT_FOR_SLEEPING = 'Контроль сна!'

OOPS = 'oops'

PHYSICAL_ACTIVITY = (
    ('ABSENT', 'Отсутствует'),
    ('INFREQUENT', 'Редкие тренировки'),
    ('MODERATE', 'Умеренная активность'),
    ('INTENSE', 'Интенсивные тренировки'),
    ('PROFESSIONAL', 'Профессиональный спорт'),
)
PHYS_ACTIV_KOEF = {
    'ABSENT': 1.2,
    'INFREQUENT': 1.375,
    'MODERATE': 1.55,
    'INTENSE': 1.725,
    'PROFESSIONAL': 1.9,
}

START_URL = 't.me/{bot_username}?start=survey-canceled'
SURVEY_CONFIRMED, SURVEY_CANCELED = dict(CONFIRM).keys()
SURVEY_RESULT = (
    '<b>Ваша анкета готова.</b>🎉\n\n'
    'Имя: {name}\nПол: {gender}\nВозраст: {age}\nРост:{height}\n'
    'Вес:{weight}\nE-mail: {email}\n'
    'Текущая физическая активность: {activity}\n'
    'Преследуемая цель: {purpose}\n'
)

TEXT_FOR_DIET = 'Время покушать, жми кнопку "Контроль Калорий"!'
TEXT_FOR_TRAINING = 'Время для тренировки, жми кнопку "К тренировкам"!'
TEXT_FOR_SLEEPING = 'Время для сна, жми кнопку "Контроль сна"!'
TIME_TRAINING_FOR_SCHEDULER = '11, 14, 19'
TIME_SLEEP_FOR_SCHEDULER = '8, 23'
TIME_CALORIES_FOR_SCHEDULER = '8, 12, 18'

SLEEP = 'sleep'

WEIGHT_COEF_MAN = 13.4
WEIGHT_COEF_WOMAN = 9.2
WORKOUT = 'workout'
WORKOUT_COURSE = 'workout_course'
WORKOUTS = 'workouts'
WORKOUT_TYPE = (
    ('Cardio', 'Кардио'),
    ('Legs', 'Ноги'),
    ('Back', 'Спина, плечи, трицепс'),
    ('Front', 'Грудь, бицепс'),
)
