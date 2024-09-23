"""Модуль основного меню."""

from aiogram import Bot
from aiogram.types import BotCommand

from app.core.constants import MAIN_MENU_COMMANDS


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)
