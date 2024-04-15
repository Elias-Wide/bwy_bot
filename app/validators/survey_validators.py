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
        value = int(value)
    except ValueError:
        raise DisallowedHumanParameterError(
            INVALID_LITERAL_ERROR.format(value),
        )
    min_value, max_value = valid_range
    if min_value > value or value > max_value:
        raise DisallowedHumanParameterError(
            OUT_OF_ALLOWED_RANGE_ERROR.format(value, min_value, max_value),
        )
    return value
