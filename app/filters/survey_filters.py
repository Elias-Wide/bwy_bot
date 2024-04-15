from aiogram.types import Message
from email_validator import EmailNotValidError, validate_email

from app.core.constants import (
    ALLOWED_AGE_RANGE,
    ALLOWED_HEIGHT_RANGE,
    ALLOWED_WEIGHT_RANGE,
)
from app.core.logging import get_logger
from app.exceptions.survey_exceptions import DisallowedHumanParameterError
from app.validators.survey_validators import validate_number_value

logger = get_logger(__name__)


def filter_invalid_email(message: Message) -> str | None:
    try:
        return validate_email(message.text).normalized
    except EmailNotValidError as error:
        logger.warning(error)
        return None


def filter_invalid_height(
    message: Message,
    valid_range: tuple[int, int] = ALLOWED_HEIGHT_RANGE,
) -> int | None:
    try:
        return validate_number_value(message.text, valid_range)
    except DisallowedHumanParameterError as error:
        logger.warning(error)
        return None


def filter_invalid_weight(
    message: Message,
    valid_range: tuple[int, int] = ALLOWED_WEIGHT_RANGE,
) -> int | None:
    try:
        return validate_number_value(message.text, valid_range)
    except DisallowedHumanParameterError as error:
        logger.warning(error)
        return None


def filter_invalid_age(
    message: Message,
    valid_range: tuple[int, int] = ALLOWED_AGE_RANGE,
) -> int | None:
    try:
        return validate_number_value(message.text, valid_range)
    except DisallowedHumanParameterError as error:
        logger.warning(error)
        return None
