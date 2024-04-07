from aiogram.types import FSInputFile

from app.core.config import BASE_DIR
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _get_videos(category: str) -> list[FSInputFile]:
    content_path = BASE_DIR.parent.joinpath('upload', category)
    videos = [FSInputFile(path) for path in list(content_path.glob('*.mp4'))]
    return videos


async def _get_banner(menu_name: str) -> FSInputFile:
    content_path = BASE_DIR.joinpath('static', menu_name + '.jpg')
    return FSInputFile(content_path)
