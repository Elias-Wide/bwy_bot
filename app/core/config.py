from pathlib import Path, PosixPath

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    telegram_bot_token: str = '**********:***********************************'
    base_dir: PosixPath = Path(__file__).resolve().parent.parent

    class Config:
        env_file = '.env'


settings = Settings()
