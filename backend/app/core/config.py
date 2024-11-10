from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title = "Продуктовый помощник"
    database_url: str
    secret: str = "SECRET"

    class Config:
        env_file: str = ".env"


settings = Settings()
