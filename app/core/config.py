from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    telegram_bot_token: str = '**********:***********************************'
    webhook_host: str = '****************.ngrok-free.app'
    webhook_mode: bool = False
    database_url: str = 'sqlite+aiosqlite:///./bwy_bot.db'
    username: str = 'mail@mail.ru'
    password: str = '***********'

    class Config:
        env_file = '.env'


settings = Settings()
