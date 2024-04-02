from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    telegram_bot_token: str = '**********:***********************************'
    webhook_url: str = 'https://b2e3-217-28-217-133.ngrok-free.app'

    class Config:
        env_file = '.env'


settings = Settings()
