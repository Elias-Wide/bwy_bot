from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    telegram_bot_token: str = '**********:***********************************'
    webhook_host: str = '****************.ngrok-free.app'

    class Config:
        env_file = '.env'


settings = Settings()
