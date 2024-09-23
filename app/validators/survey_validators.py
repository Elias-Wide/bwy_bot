"""
Модуль валидаторов.

Functions:
    validate_number_value: валидация цифр в строке
    validate_local_time: валидация времени

"""

from app.core.constants import (
    INVALID_LITERAL_ERROR,
    INVALID_TIME_MESSAGE,
    OUT_OF_ALLOWED_RANGE_ERROR,
)
from app.exceptions.survey_exceptions import DisallowedHumanParameterError


def validate_number_value(
    value: str,
    valid_range: tuple[int, int],
) -> int | None:
    """Валидация числовых значений.

    Принимает строку, которая должна содержать только цифры,
    преобразует строку и возвращает значение типа int.
    Если есть невалидные символы или значение полученного числа выходит
    за рамки допустимого диапазона - поднимается соответствующая ошибка

    Args:
        value (str): строка
        valid_range (tuple[int, int]): диапазон допустимых значений

    Raises:
        DisallowedHumanParameterError: возвращает число(int) | None при ошибке

    Returns:
        int | None
    """
    try:
        number_value = int(value)
    except ValueError as error:
        raise DisallowedHumanParameterError(
            INVALID_LITERAL_ERROR.format(value),
        ) from error
    if number_value not in range(*valid_range):
        raise DisallowedHumanParameterError(
            OUT_OF_ALLOWED_RANGE_ERROR.format(number_value, *valid_range),
        )
    return number_value


def validate_local_time(
    value: str,
    utc_time: str,
) -> str | None:
    """Валидация локального времени пользователя.

    Args:
        value (str): локальное время в строковом представлении
        utc_time (str):  время UTC в строковом представлении

    Raises:
        DisallowedHumanParameterError

    Returns:
        str | None: возвращает строку | None при ошибке
    """
    if value is not None:
        if value.split(':')[1] != utc_time.split(':')[1]:
            raise DisallowedHumanParameterError(
                INVALID_TIME_MESSAGE.format(value),
            )
        if int(value.split(':')[0]) not in range(0, 24):
            raise DisallowedHumanParameterError(
                OUT_OF_ALLOWED_RANGE_ERROR.format(
                    value.split(':')[0],
                    range(0, 24),
                ),
            )
    return value
