from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URI: str = "postgresql://localhost/test"


settings = Settings()
