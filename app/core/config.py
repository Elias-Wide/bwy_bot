from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR.parent / 'upload'


class Settings(BaseSettings):

    telegram_bot_token: str = '**********:***********************************'
    webhook_host: str = '****************.ngrok-free.app'
    webhook_mode: bool = False
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    username: str = 'mail@mail.ru'
    password: str = '***********'
    admin_auth_secret: str = '*********************'

    class Config:
        env_file = '.env'


settings = Settings()
