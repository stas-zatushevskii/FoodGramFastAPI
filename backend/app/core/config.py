from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title = 'Продуктовый помощник'
    database_url: str

    class Config:
        env_file: str = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()