from app.exceptions.survey_exceptions import DisallowedHumanParameterError

INVALID_LITERAL_ERROR = (
    'Переданную строку "{}" не возможно преобразовать в целое число.'
)
OUT_OF_ALLOWED_RANGE_ERROR = (
    'Введенное число {} не принадлежит диапазону {} - {} включительно.'
)


def validate_number_value(
    value: str,
    valid_range: tuple[int, int],
) -> int | None:
    try:
        number_value = int(value)
    except ValueError:
        raise DisallowedHumanParameterError(
            INVALID_LITERAL_ERROR.format(value),
        )
    if number_value not in range(*valid_range):
        raise DisallowedHumanParameterError(
            OUT_OF_ALLOWED_RANGE_ERROR.format(number_value, *valid_range),
        )
    return number_value
