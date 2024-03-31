from aiogram import Dispatcher, Bot,  types
from aiogram.filters import Command


TOKEN = '123456789:***************************'
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(message)
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
    await message.answer(f'Hi, {message.from_user.full_name}, выберите нужное', reply_markup=keyboard)
