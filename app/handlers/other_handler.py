from aiogram import Router
from aiogram.types import Message

router = Router()
ADMIN_EMAIL = 'any@example.com'


@router.message()
async def send_echo(message: Message) -> None:
    await message.reply(
        f'На данный момент я не поддерживаю команду {message.text} 🤷\n\n'
        f'Могу предложить вам обратиться по {ADMIN_EMAIL} с предложением по'
        ' улучшению бота или воспользоваться /help'
    )
