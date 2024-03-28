import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

'не забыть создать в .env переменн окружения TOKEN своего бота'
TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        'start',
        reply_markup=types.ReplyKeyboardRemove()
    )
    kb = [
        [types.KeyboardButton(text="Анкетирование")],
        [types.KeyboardButton(text="Калории")],
        [types.KeyboardButton(text="Сон")],
        [types.KeyboardButton(text="Тренировки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Выберите нужное", reply_markup=keyboard)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
