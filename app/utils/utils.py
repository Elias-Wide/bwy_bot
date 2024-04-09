from aiogram.types import FSInputFile

from app.core.config import BASE_DIR
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _get_videos(category: str) -> list[FSInputFile]:
    content_path = BASE_DIR.parent.joinpath('upload', category)
    return [FSInputFile(path) for path in list(content_path.glob('*.mp4'))]


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def _get_banner(menu_name: str) -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static', menu_name + '.jpg'))


# TODO: продумать момент хранения графиков каллоража/ директория/ названия
async def _get_calorie_plot() -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static/calorie_plots', 'plot01.jpg'))
