from aiogram import Router
from aiogram.types import Message

from app.core.config import settings

router = Router()


@router.message()
async def send_echo(message: Message) -> None:
    await message.reply(
        f'На данный момент я не поддерживаю команду {message.text} 🤷\n\n'
        f'Могу предложить вам обратиться по {settings.username} с предложением'
        f' по улучшению бота или воспользоваться /help'
    )
