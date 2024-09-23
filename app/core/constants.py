"""Содержит константы, литералы употребляемые в приложении."""

from enum import Enum


class SleepMode(str, Enum):
    """Перечисления состояний."""

    DURATION = 'sleep_duration'
    GO_TO_BED = 'go_to_bed'
    SLEEP = 'sleep'
    STATISTIC = 'sleep_statistic'
    WAKE_UP = 'wake_up'
    DURATION_BTN = 'duration_btn'
    DURATION_YES = 'sleep_duration_yes'
    DURATION_NO = 'sleep_duration_no'
    GO_SLEEP_OK_BTN = 'go_sleep_ok_btn'
    WAKE_UP_OK_BTN = 'go_wake_up_btn'
    SLEEP_NOT_EXIST = 'sleep_not_exist'
    FORGOT_SET_WKUP_TIME = 'forgot_set_wkup_time'
    SLEEP_EXIST = 'sleep_exist'
    VALID = 'valid'
    NOT_TIME_WKUP = 'not_time_wkup'
    NOT_TIME_GTB = 'not_time_gtb'


SLEEP_BUTTONS = {
    'Ложусь спать': SleepMode.GO_TO_BED,
    'Проснулся': SleepMode.WAKE_UP,
    'Продолжительность сна': SleepMode.DURATION,
    'Статистика': SleepMode.STATISTIC,
}

SLEEP_BUTTONS_ANSWER = {
    'ОК👍': SleepMode.GO_TO_BED,
    'Да👍': SleepMode.DURATION_YES,
    'Нет👎': SleepMode.DURATION_NO,
}
OK_BTN, YES_BTN, NO_BTN = (value for value in SLEEP_BUTTONS_ANSWER.keys())


class SurveyQuestions(str, Enum):
    """Перечисление вопросов анкеты."""

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
    LOCATION = (
        'Для автоопределения Вашего часового пояса поделитесь локацией '
        'или введите Ваше текущее локальное время вручную в 24-часовом '
        'формате, разделяя часы и минуты двоеточием, 14:35, к примеру.'
    )


SHARE_LOCATION_BTN_TEXT = 'Поделиться'
LOCATION = 'location'


ACTIVITY_KEYBOARD_SIZE = (1,)
ACTIVITY_PURPOSE = (
    ('GO_SLIM', 'Сброс массы'),
    ('KEEP_LEVEL', 'Поддержание массы'),
    ('ADD_MASS', 'Набор массы'),
)
AGE_COEF_MAN = 5.7
AGE_COEF_WOMAN = 4.3
ALLOWED_AGE_RANGE = (14, 56)
ALLOWED_HEIGHT_RANGE = (100, 250)
ALLOWED_WEIGHT_RANGE = (20, 500)
AM_NOON_PM = (
    ('AM', '11:00'),
    ('NOON', '14:00'),
    ('PM', '19:00'),
)

BACK = 'Назад👈'
BACKWARD = 'backward'
BUTTONS = {
    'Сон💤': 'sleep',
    'Питание🥦': 'diet',
    'Тренировки🏋‍♂️': 'workouts',
    'Напоминания🛠': 'settings',
}

CAL_COEF_MAN = 88.36
CAL_KOEF_WOMAN = 447.6
COEF_TO_SLIM = 0.85
COEF_ADD_MASS = 1.2
COEF_ROUND = 2

INTRO_SLEEP_TEXT = (
    'Если Вы ложитесь спать или только что проснулись, нажмите '
    'соответствующие кнопки? Мы запишем текущее время как '
    'время начала сна или пробуждения. '
    'Или можете ввести сразу количество часов сегодняшнего '
    'ночного сна.'
)

INTRO_SETTINGS_TEXT = (
    'Здесь вы можете управлять напоминаними. '
    'Нажатие на соответствующую кнопку включит '
    'или отключит напоминание. '
    'Вы можете сами выбирать какими напоминаниями '
    'Вам пользоваться. '
)

CAPTIONS = {
    'main': 'Добро пожаловать в Ваш личный помощник самосовершенствования.',
    'sleep': INTRO_SLEEP_TEXT,
    'settings': INTRO_SETTINGS_TEXT,
    'stop_train': 'Тренировки',
    'stop_sleep': 'Сон',
    'stop_calorie': 'Калории',
    'workouts': '<b>Какой вид тренировки предпочитаете?</b>',
    'train': 'Выберите тренировку',
    'diet': 'Ваша норма калорий на день {} Ккал',
    'sleep_exist': 'Сегодня вы уже записали данные своего сна.',
    'forgot_set_wkup_time': (
        'Упс, вчера вы не записали, когда легли спать.\n\n'
        'Воспользуйтесь кнопкой "Продолжительность сна".'
    ),
    'sleep_not_exist': (
        'Упс, кажется, вы уже отмечались сегодня.\n\n'
        'Если вчера забыли записать время, когда легли, '
        'то воспользуйтесь разделом "Продолжительность сна", чтобы записать '
        'данные за прошедшую ночь.'
    ),
    'not_time_wkup': (
        'Не время просыпаться!\n\n'
        'Если забыли в прошлый раз зафиксировать время, когда проснулись - '
        'используйте раздел "Продолжительность сна".'
    ),
    'not_time_gtb': (
        'Еще рано, чтобы записывать время сна.\n\n'
        'Если забыли зафиксировать время, когда легли вчера \n'
        '(или сегодня ночью) - используйте раздел "Продолжительность сна".'
    ),
    'oops': {
        1: 'В данный момент для Вас нет тренировки...',
        2: 'В данный момент для Вас нет тренировки...',
        3: 'В данный момент для Вас нет упражнений к этой тренировке...',
    },
    'oops_diet': 'В данный момент для вас нет графика КБЖУ...',
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
FORWARD = 'forward'

GENDER = (
    ('MALE', 'Мужчина'),
    ('FEMALE', 'Женщина'),
)
GENDER_OR_NONE = GENDER + (('NOT_SELECTED', 'Не выбрано'),)
GENDER_NOT_SELECTED = list(dict(GENDER_OR_NONE).keys())[
    list(dict(GENDER_OR_NONE).values()).index('Не выбрано')
]

HASH_PASSWORD = 'nkajipfncu89288)*&^guyb'
HEIGHT_COEF_MAN = 4.8
HEIGHT_COEF_WOMAN = 3.1

INTRO_SURVEY_TEXT = (
    '<b>Привет! С чем поможет этот фитнес бот?</b>\n'
    'Подскажет количество каллорий 🍕, напомнит '
    'о здоровом сне 🛏, подскажет и покажет тренировку. 🏃‍♂️ '
    'Для хорошей подсказки ему необходимо знать немного о Вас.'
    '\n😜\n'
)
INVALID_NUM_MESSAGE = (
    'Введите целое число в диапазоне от {} до {} включительно'
)
INVALID_EMAIL_MESSAGE = 'Ошибка при вводе email. Попробуйте снова.'
INVALID_LITERAL_ERROR = (
    'Переданную строку "{}" не возможно преобразовать в целое число.'
)
INVALID_TIME_MESSAGE = 'Ошибка при вводе времени "{}". Попробуйте снова.'


MAIN_MENU = 'main'
MAIN_MENU_COMMANDS = {
    '/start': 'Перезапуск бота',
    '/help': 'Справка',
}

MOSCOW = 'Europe/Moscow'
UTC = 'UTC'
TIMEZONE_RU = {
    1: 'Europe/London',
    2: 'Europe/Kaliningrad',
    3: 'Europe/Moscow',
    4: 'Europe/Samara',
    5: 'Asia/Yekaterinburg',
    6: 'Asia/Omsk',
    7: 'Asia/Krasnoyarsk',
    8: 'Asia/Irkutsk',
    9: 'Asia/Yakutsk',
    10: 'Asia/Vladivostok',
    11: 'Asia/Magadan',
    12: 'Asia/Kamchatka',
}

NEXT = 'След. ➡️'

OUT_OF_ALLOWED_RANGE_ERROR = (
    'Введенное число {} не принадлежит диапазону {} - {} включительно.'
)


KB_TEXT_FOR_DIET = 'Контроль Калорий!'
KB_TEXT_FOR_TRAINING = 'К тренировкам!'
KB_TEXT_FOR_SLEEPING = 'Контроль сна!'

OOPS = 'oops'
OOPS_DIET = 'oops_diet'
DIET_CRUD_ERROR = 'В базе для {}, {} и {} нет графика.'
WORKOUT_CRUD_ERROR = ('В базе для {} и {} нет тренировок группы {}.',)


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

RANDOM_WORKOUT = 'Случайная тренировка'

SURVEY_CONFIRMED, SURVEY_CANCELED = dict(CONFIRM).keys()

SURVEY_RESULT = (
    '<b>Ваша анкета готова.</b>🎉\n\n'
    'Имя: {name}\nПол: {gender}\nВозраст: {age}\nРост:{height}\n'
    'Вес:{weight}\nE-mail: {email}\n'
    'Текущая физическая активность: {activity}\n'
    'Преследуемая цель: {purpose}\n'
    'Ваша локация:{location}\n'
)
SURVEY_TZ = 'Ваша таймзона UTC '

TEXT_FOR_DIET_SIMPLE = 'Время подкрепиться 🍽, жми кнопку "Контроль Калорий"!'

TEXT_FOR_DIET = {
    8: 'Время завтракать 🍜, жми кнопку "Контроль Калорий"!',
    13: 'Время обедать 🍝, жми кнопку "Контроль Калорий"!',
    18: 'Время ужинать 🥗, жми кнопку "Контроль Калорий"!',
}
TEXT_FOR_TRAINING = 'Время для тренировки 🏋‍♂️, жми кнопку "К тренировкам"!'
TEXT_FOR_SLEEPING = 'Время для контроля сна 💤, жми кнопку "Контроль сна"!'
TIME_TRAINING_FOR_SCHEDULER = '10, 15, 19'
TIME_SLEEP_FOR_SCHEDULER = '11, 22'
TIME_CALORIES_FOR_SCHEDULER = '8, 13, 18'
SCHEDULE_JOB_HOUR = ', '.join([str(x) for x in range(0, 24)])

SOME_ADV_TEXT = 'Some advertisment text'

SECONDS_IN_HOUR = 3600
SLEEP = 'sleep'
ADV = 'advertisment'
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

USER_DATE_FORMAT = '%H:%M'
DB_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
SLEEP_STATISTIC_FORMAT = '%d.%m.%Y %H:%M'

SLEEP_MAIN_MENU = (
    ('go_to_bed', 'Ложусь спать'),
    ('wake_up', 'Проснулся'),
    ('sleep_duration', 'Продолжительность сна'),
    ('sleep_statistic', 'Статистика'),
)

SETTINGS = 'settings'
SETTINGS_BUTTONS = {
    'Тренировки': 'stop_train',
    'Сон': 'stop_sleep',
    'Калории': 'stop_calorie',
}

STATE_TRAIN = 'Напоминание про тренировку - '
STATE_SLEEP = 'Напоминание про сон - '

STATE_CALORIES = 'Напоминание про калории - '
TRAIN = 'train'
REMINDER_STATE_TRUE = 'ВЫКЛ'
REMINDER_STATE_FALSE = 'ВКЛ'
DEFAULT_SLEEP_DURATION = 8

USER_DATE_FORMAT = '%H:%M'
GO_TO_BED_TEXT = 'Ваше время отхода ко сну: '
WAKE_UP_TEXT = 'Вы проснулись в: '
SLEEP_DURATION_QUESTION_TEXT = 'Сегодня ночью Вы спали {} часов?'
SET_DEFAULT_SLEEP_DURATION_QUESTION = (
    'Ответьте Да или Нет. Мы запишем Ваши данные о сне.'
)

STATISTIC_TITLE_TEXT = 'Коротко о Вашем сне:\n\n'
HEALTHY_SLEEP = 'Здоровый сон👍'
UNHEALTHY_SLEEP = 'Недосып👎'

UPLOAD_FILE_NAME_LEN = 100
INVALID_FILE_NAME_LEN_MESSAGE = (
    f'Длина именифайла больше {UPLOAD_FILE_NAME_LEN} символов'
)
UPLOAD_VIDEO_MAX_SIZE = 1024000
UPLOAD_IMAGE_MAX_SIZE = 172000
INVALID_VIDEO_MAX_SIZE_MESSAGE = (
    f'Размер файла больше {UPLOAD_VIDEO_MAX_SIZE/1000} Kb'
)
INVALID_IMAGE_MAX_SIZE_MESSAGE = (
    f'Размер файла больше {UPLOAD_IMAGE_MAX_SIZE/1000} Kb'
)
INVALID_VIDEO_FORMAT_MESSAGE = 'Файл дожен быть формата mp4'
INVALID_IMAGE_FORMAT_MESSAGE = 'Файл дожен быть формата jpeg'
INVALID_UPLOAD_FILE_NAME_MESSAGE = (
    'Только английские буквы, цифры, подчеркивание, дефис без пробелов',
)


class ScheduleReminder(str, Enum):
    """Перечисления названий напоминалка."""

    WORKOUTS = (WORKOUTS,)
    DIET = (DIET,)
    SLEEP = (SLEEP,)
    ADV = (ADV,)


PLURAL_NAME_USER = 'Пользователи'
PLURAL_NAME_EXERCISE = 'Упражнения(видео)'
PLURAL_NAME_WORKOUT_EXERCISE = 'Упражнения в тренировках'
PLURAL_NAME_WORKOUT = 'Тренировки'
PLURAL_NAME_SCHEDULE = 'Напоминания'
PLURAL_NAME_SLEEP = 'Сон(статистика)'
PLURAL_NAME_CALORIE = 'Калории(картинки в static)'
PLURAL_NAME_ADVERTISEMENT = 'Рекламные анонсы'
