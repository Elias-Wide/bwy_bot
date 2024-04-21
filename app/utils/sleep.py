from datetime import datetime

from app.utils.const import (
    DEFAULT_SLEEP_DURATION,
    GO_TO_BED_TEXT,
    NEGATIVE_SLEEP_TIP,
    POSITIVE_SLEEP_TIP,
    SET_DEFAULT_SLEEP_DURATION_QUESTION,
    SLEEP_DURATION_QUESTION_TEXT,
    STATISTIC_TITLE_TEXT,
    USER_DATE_FORMAT,
    WAKE_UP_TEXT,
)


def go_to_bed_time() -> str:
    return f'{GO_TO_BED_TEXT}{datetime.now().strftime(USER_DATE_FORMAT)}'


def wake_up_time() -> str:
    return f'{WAKE_UP_TEXT}{datetime.now().strftime(USER_DATE_FORMAT)}'


def get_sleep_duration() -> str:
    sleep_duration = 8.5  # TODO вычислять
    if not sleep_duration:
        return (
            f'{SLEEP_DURATION_QUESTION_TEXT.format(sleep_duration)}'
            f'{SET_DEFAULT_SLEEP_DURATION_QUESTION}'
        )
    if sleep_duration >= DEFAULT_SLEEP_DURATION:
        return (
            f'{SLEEP_DURATION_QUESTION_TEXT.format(sleep_duration)}'
            f'{POSITIVE_SLEEP_TIP}'
        )
    return (
        f'{SLEEP_DURATION_QUESTION_TEXT.format(sleep_duration)}'
        f'{NEGATIVE_SLEEP_TIP}'
    )


def get_sleep_statistic() -> str:
    sleep_week_duration = (  # TODO вычислять
        'вчера не менее 8 часов, \n'
        'позавчера не менее 8 часов, \n'
        '16.04.2024 не менее 8 часов, \n'
        '15.04.2024 МЕНЕЕ 8 часов, \n'
        '14.04.2024 МЕНЕЕ 8 часов, \n'
        '13.04.2024 не менее 8 часов, \n'
        '12.04.2024 не менее 8 часов \n\n'
    )
    return STATISTIC_TITLE_TEXT.format(sleep_week_duration)
