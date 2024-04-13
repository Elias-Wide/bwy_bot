from aiogram.types import FSInputFile

from app.core.config import BASE_DIR


async def _get_videos() -> list[FSInputFile]:
    return [
        FSInputFile(path)
        for path in list(UPLOAD_DIR.glob('*.mp4'))
    ]


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def _get_banner(menu_name: str) -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static', menu_name + '.jpg'))


# TODO: продумать момент хранения графиков каллоража/ директория/ названия
async def _get_calorie_plot() -> FSInputFile:
    return FSInputFile(
        BASE_DIR.joinpath('static/calorie_plots', 'plot' + '01' + '.jpg'),
    )


async def _calculation_of_calories() -> int:
    return 1200
