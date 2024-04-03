from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
import logging
from pathlib import Path
from app.core.config import settings
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)

TOKEN = settings.telegram_bot_token
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Bot is running!')
    logger.info(message)
    await message.answer(
        'start',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    kb = [
        [types.KeyboardButton(text='Анкетирование')],
        [types.KeyboardButton(text='Калории')],
        [types.KeyboardButton(text='Сон')],
        [types.KeyboardButton(text='Тренировки')],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(
        f'Hi, {message.from_user.full_name},выберите нужное',
        reply_markup=keyboard,
    )
