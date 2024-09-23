"""Здесь настройки приложения."""

from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR.parent / 'upload'
STATIC_DIR = BASE_DIR / 'static'


class Settings(BaseSettings):
    """Содержит основные настройки приложения."""

    telegram_bot_token: str = '0000000000:El55gRI4rikAAHUdelfhmd......'
    webhook_host: str | None = None
    webhook_mode: bool = False
    database_url: str = 'sqlite+aiosqlite:///./some.db'
    username: str = 'mail@mail.ru'
    password: str = 'секрет_world'
    admin_auth_secret: str = 'Какая-то_Секret_Sting!'

    class Config:
        """Имя файла содержащего сами настройки."""

        env_file = '.env'


settings = Settings()
