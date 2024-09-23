"""Модуль валидаторов админки.

Functions:
    validate_upload_video: валидация загружаемого видео
    validate_upload_image: валидация загружаемого изображения
"""

import re

from fastapi_storages.integrations.sqlalchemy import FileType

from app.core.constants import (
    INVALID_FILE_NAME_LEN_MESSAGE,
    INVALID_IMAGE_FORMAT_MESSAGE,
    INVALID_IMAGE_MAX_SIZE_MESSAGE,
    INVALID_UPLOAD_FILE_NAME_MESSAGE,
    INVALID_VIDEO_FORMAT_MESSAGE,
    INVALID_VIDEO_MAX_SIZE_MESSAGE,
    UPLOAD_FILE_NAME_LEN,
    UPLOAD_IMAGE_MAX_SIZE,
    UPLOAD_VIDEO_MAX_SIZE,
)
from app.exceptions.admin_exceptions import (
    ImageValidationError,
    VideoValidationError,
)


async def validate_upload_video(data: dict) -> None:
    """валидация загружаемого в админку видео.

    Осуществляется проверка на валидность файла по допустимой длине названия,
    формату имени, максимально допустимому объему передаваемых данных и
    формату видео.

    Args:
        data (dict): словарь с данными, переданными в запросе при загрузке

    Raises:
        VideoValidationError: ошибка валидации видео, передается сообщение,
        какой параметр не прошел проверку.
    """
    if len(data['video'].filename) > UPLOAD_FILE_NAME_LEN:
        raise VideoValidationError(INVALID_FILE_NAME_LEN_MESSAGE)
    if data['video'].size > UPLOAD_VIDEO_MAX_SIZE:
        raise VideoValidationError(INVALID_VIDEO_MAX_SIZE_MESSAGE)
    if data['video'].content_type not in ["video/mp4"]:
        raise VideoValidationError(INVALID_VIDEO_FORMAT_MESSAGE)
    if not re.match("^[A-Za-z0-9_-]*.mp4$", data['video'].filename):
        raise VideoValidationError(INVALID_UPLOAD_FILE_NAME_MESSAGE)


async def validate_upload_image(image: FileType) -> None:
    """валидация загружаемого в админку изображения.

    Осуществляется проверка на валидность файла по допустимой длине
    названия, корректности имени, максимально допустимому объему
    передаваемых данных и формату.

    Args:
        data (dict): словарь с данными, переданными в запросе при загрузке

    Raises:
        VideoValidationError: ошибка валидации изображения,
        возвращает сообщение, какой параметр не прошел проверку.
    """
    if len(image.filename) > UPLOAD_FILE_NAME_LEN:
        raise ImageValidationError(INVALID_FILE_NAME_LEN_MESSAGE)
    if image.size > UPLOAD_IMAGE_MAX_SIZE:
        raise ImageValidationError(INVALID_IMAGE_MAX_SIZE_MESSAGE)
    if image.content_type not in [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
    ]:
        raise ImageValidationError(INVALID_IMAGE_FORMAT_MESSAGE)
    if not re.match(
        "^[A-Za-z0-9_-]*$",
        image.filename.split('.')[0],
    ):
        raise ImageValidationError(INVALID_UPLOAD_FILE_NAME_MESSAGE)
